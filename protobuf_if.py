# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/30 20:20
# @File     : protobuf_if.py
# @Project  : radar_fusion
import ConfigConstantData
import presentationLayer
import all_data_pb2
import meta_pb2

class All_Data:
    def __init__(self, all_data_buf):
        all_data = all_data_pb2.Data()
        all_data.ParseFromString(all_data_buf)
        self.frame_id = all_data.frame_id
        self.radar_obj_list = all_data.structure_radar.radar_object
        self.redar_obj_cntr = all_data.structure_radar.num_obj

        self.fused_obj_list = all_data.structure_fusion.fused_object
        self.fused_obj_cntr = all_data.structure_fusion.num_obj

        self.radar_obj_list_draw = self.get_radar_object_draw_list()
        self.fused_obj_list_draw = self.get_fused_object_draw_list()

    def get_radar_object_draw_list(self):
        radar_obj_list_draw = []
        for i in range(self.redar_obj_cntr):
            radar_obj = self.radar_obj_list[i]
            obj_draw_info = presentationLayer.MyCuboid(width=radar_obj.width, length=radar_obj.length,
                                                       x=radar_obj.object_distlong, y=radar_obj.object_distlat,z=0,
                                                       _type=radar_obj.object_class,
                                                       _id=radar_obj.object_id,
                                                       _stMovement=0,  # ?
                                                       _probability=0,
                                                       _absV_x=radar_obj.object_vrellong,
                                                       _absV_y=radar_obj.object_vrelat)
            obj_draw_info.setHight(0)
            radar_obj_list_draw.append(obj_draw_info)


        return radar_obj_list_draw

    def get_fused_object_draw_list(self):
        fused_obj_list_draw = []
        for i in range(self.fused_obj_cntr):
            fused_obj = self.fused_obj_list[i]
            obj_draw_info = presentationLayer.MyCuboid(width=fused_obj.width, length=fused_obj.length,
                                                       x=fused_obj.position.x, y=fused_obj.position.y,
                                                       z=fused_obj.position.z,
                                                       _type=fused_obj.type,
                                                       _id=fused_obj.track_id,
                                                       _stMovement=0,  # ?
                                                       _probability=fused_obj.fused_obj.conf,
                                                       _absV_x=fused_obj.vel.vx,
                                                       _absV_y=fused_obj.vel.vy)
            obj_draw_info.setHight(fused_obj.height)
            fused_obj_list_draw.append(obj_draw_info)

        return fused_obj_list_draw


class Meta:
    def __init__(self, meta_buf):
        meta = meta_pb2.Meta()
        meta.ParseFromString(meta_buf)
        self.frame_id = meta.frame_id
        self.version = meta.version
        self.meta_data = meta.data

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
                    box_2d.set_color(presentationLayer.My_cv2_Color.Red)
                    box_2d_list.append(box_2d)

                if box.conf>0:
                    points = []
                    points.append((box.upper_lb.x, box.upper_lb.y))
                    points.append((box.upper_rb.x, box.upper_rb.y))
                    points.append((box.upper_rt.x, box.upper_rt.y))
                    points.append((box.upper_lt.x, box.upper_lt.y))
                    points.append((box.lower_lb.x, box.lower_lb.y))
                    points.append((box.lower_rb.x, box.lower_rb.y))
                    points.append((box.lower_rt.x, box.lower_rt.y))
                    points.append((box.lower_lt.x, box.lower_lt.y))
                    box_3d = presentationLayer.Box_3D(points=points)
                    box_3d.set_text("id:%d" % obstacle.id)
                    box_3d.set_color(presentationLayer.My_cv2_Color.Green)
                    box_3d_list.append(box_3d)

        print('mata 3D box conter is:', len(box_3d_list))
        print('mata 2D box conter is:', len(box_2d_list))
        return box_2d_list, box_3d_list


