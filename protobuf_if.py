# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/30 20:20
# @File     : protobuf_if.py
# @Project  : radar_fusion
import ConfigConstantData
import Radar_vcs2pixel
import presentationLayer
import all_data_pb2
import meta_pb2
import Radar_vcs2pixel

map_color2String = {
    0 : 'vehicle',
    1: 'pedestrian',
    2: 'cycle'
}

def get_typestr_by_type(type):
    # 判断是否存在map
    str = ''
    if type in map_color2String:
     str =  map_color2String[type]
    else:
        str = 'unknown'
    return str

class All_Data:
    def __init__(self, all_data_buf):
        all_data = all_data_pb2.Data()
        all_data.ParseFromString(all_data_buf)
        self.frame_id = all_data.frame_id
        self.obj_color = presentationLayer.My_cv2_Color.Green
        self.radar_obj_list = all_data.structure_radar.radar_object
        self.redar_obj_cntr = all_data.structure_radar.num_obj

        self.fused_obj_list = all_data.structure_fusion.fused_object
        self.fused_obj_cntr = all_data.structure_fusion.num_obj

        self.radar_obj_list_draw = self.get_radar_object_draw_list()
        self.fused_obj_box2D, self.fused_obj_box3D = self.get_fused_object_draw_list()

    def get_radar_object_draw_list(self):
        radar_obj_list_draw = []
        for i in range(self.redar_obj_cntr):
            radar_obj = self.radar_obj_list[i]
            world_info_distlong = radar_obj.object_distlong
            world_info_distlat = radar_obj.object_distlat

            x,y = Radar_vcs2pixel.vcs2pixel(world_info_distlong, world_info_distlat)
            length = radar_obj.length
            width = radar_obj.width
            x = x - length/2
            y = y - width/2
            id = radar_obj.object_id
            box_2d = presentationLayer.Box_2D(x, y, length, width)
            box_2d.set_text('radar obj id'+str(id))
            box_2d.set_text(self.obj_color)
            radar_obj_list_draw.append(box_2d)

        return radar_obj_list_draw

    def get_fused_object_draw_list(self):
        fused_2dBox_lit = []
        fused_3dBox_lit = []
        for i in range(self.fused_obj_cntr):
            fused_obj = self.fused_obj_list[i]
            id = fused_obj.track_id
            type = fused_obj.type
            conf = fused_obj.conf
            length = fused_obj.length
            width = fused_obj.width
            height = fused_obj.height
            velocity = fused_obj.vel
            acceleration = fused_obj.acc


            x0 = fused_obj.rect.left
            y0 = fused_obj.rect.top
            x1 = fused_obj.rect.right
            y1 = fused_obj.rect.bottom
            box_2d = presentationLayer.Box_2D(x0, y0, x1-x0, y1-y0)
            box_2d.set_text('fused obj id:'+str(id) + ' , type:'+get_typestr_by_type(type) + ',  conf:'+str(conf))
            box_2d.set_color(self.obj_color)
            fused_2dBox_lit.append(box_2d)

            if conf>0:
                box = fused_obj.box
                points=[]
                points.append((int(box.upper_lb.x), int(box.upper_lb.y)))
                points.append((int(box.upper_rb.x), int(box.upper_rb.y)))
                points.append((int(box.upper_rt.x), int(box.upper_rt.y)))
                points.append((int(box.upper_lt.x), int(box.upper_lt.y)))
                points.append((int(box.lower_lb.x), int(box.lower_lb.y)))
                points.append((int(box.lower_rb.x), int(box.lower_rb.y)))
                points.append((int(box.lower_rt.x), int(box.lower_rt.y)))
                points.append((int(box.lower_lt.x), int(box.lower_lt.y)))

                box_3d = presentationLayer.Box_3D(points)
                box_3d.set_text("id:%d" % id)
                box_3d.set_color(self.obj_color)
                fused_3dBox_lit.append(box_3d)

        return fused_2dBox_lit, fused_3dBox_lit


class Meta:
    def __init__(self, meta_buf):
        meta = meta_pb2.Meta()
        meta.ParseFromString(meta_buf)
        self.frame_id = meta.frame_id
        self.version = meta.version
        self.meta_data = meta.data

        self.obj_color = presentationLayer.My_cv2_Color.Red

        self.obj2Dbox_list,self.obj3Dbox_list = self.get_3DBox_draw_List()
    def b_3D_pos_valid(self, left, right, top, bottom):
        pass

    def b_2D_pos_valid(self,x0,y0,x1,y1):
        return x0>=0 and y0>=0 and x1>=x0 and y1>=y0 and x1<=ConfigConstantData.pic_width and y1<=ConfigConstantData.pic_height

    def get_3DBox_draw_List(self): # world_info
        box_2d_list = []
        box_3d_list = []
        obs = self.meta_data.structure_perception.obstacles
        if len(obs)>0: # each camera device has a obs
            obj_nr = len(obs[0].obstacle)

            for i in range(obj_nr):
                obstacle = obs[0].obstacle[i]
                rect = obstacle.img_info.rect
                box = obstacle.img_info.box
                if rect:
                    x = rect.left
                    y = rect.top
                    length = rect.right - rect.left
                    width = rect.bottom - rect.top
                    box_2d = presentationLayer.Box_2D(x=x, y=y, length=length, width=width)
                    box_2d.set_text("id:%d" % obstacle.id)
                    box_2d.set_color(self.obj_color)
                    box_2d_list.append(box_2d)

                if box.conf>0:
                    points = []
                    points.append((int(box.upper_lb.x), int(box.upper_lb.y)))
                    points.append((int(box.upper_rb.x), int(box.upper_rb.y)))
                    points.append((int(box.upper_rt.x), int(box.upper_rt.y)))
                    points.append((int(box.upper_lt.x), int(box.upper_lt.y)))
                    points.append((int(box.lower_lb.x), int(box.lower_lb.y)))
                    points.append((int(box.lower_rb.x), int(box.lower_rb.y)))
                    points.append((int(box.lower_rt.x), int(box.lower_rt.y)))
                    points.append((int(box.lower_lt.x), int(box.lower_lt.y)))
                    box_3d = presentationLayer.Box_3D(points=points)
                    box_3d.set_text("id:%d" % obstacle.id)
                    box_3d.set_color(self.obj_color)
                    box_3d_list.append(box_3d)

        print('mata 3D box conter is:', len(box_3d_list))
        print('mata 2D box conter is:', len(box_2d_list))
        return box_2d_list, box_3d_list


