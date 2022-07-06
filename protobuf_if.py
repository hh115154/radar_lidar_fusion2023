# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/30 20:20
# @File     : protobuf_if.py
# @Project  : radar_fusion
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

        self.obj3Dbox_list_draw = self.get_3DBox_draw_List()

    def get_3DBox_draw_List(self): # world_info
        box_list = []
        obs = self.meta_data.structure_perception.obstacles
        if len(obs)>0: # each camera device has a obs
            obj_nr = len(obs[0].obstacle)
            print('mata 3D box nr is:',obj_nr)
            for i in range(obj_nr):
                obstacle = obs[0].obstacle[i]
                obj = obstacle.world_info
                if obj.width>0 and obj.length>0 and obj.height>0:
                    obj_draw_info = presentationLayer.MyCuboid(width=obj.width, length=obj.length,
                                                               x=obj.position.x, y=obj.position.y,
                                                               z=obj.position.z,
                                                               _type=0,
                                                               _id=obstacle.id,
                                                               _stMovement=0,  # ?
                                                               _probability=obstacle.conf,
                                                               _absV_x=obj.vel.vx,
                                                               _absV_y=obj.vel.vy)
                    obj_draw_info.setHight(obj.height)
                    box_list.append(obj_draw_info)
        return box_list


