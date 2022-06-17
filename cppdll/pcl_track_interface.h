#pragma once
#include"pch.h"
#include"cluster_track.h"

#include"pcl_cluster.h"
#include<random>

#include<fstream>
#include<string>
#include"radar_point.h"
#include"read_csv.h"
#include"obj_540raw.h"
#include"LeastSquareMethod.h"

extern "C" _declspec(dllimport) unsigned char obj_num_outp;
extern "C" _declspec(dllimport) unsigned char obj_id_outp[80];
extern "C" _declspec(dllimport) unsigned char obj_typ_outp[80];
extern "C" _declspec(dllimport) float obj_px_outp[80];
extern "C" _declspec(dllimport) float obj_py_outp[80];
extern "C" _declspec(dllimport) float obj_pz_outp[80];
extern "C" _declspec(dllimport) float obj_vx_outp[80];
extern "C" _declspec(dllimport) float obj_vy_outp[80];
extern "C" _declspec(dllimport) float obj_vz_outp[80];
extern "C" _declspec(dllimport) float obj_length_outp[80];
extern "C" _declspec(dllimport) float obj_width_outp[80];
extern "C" _declspec(dllimport) float obj_heigth_outp[80];
extern "C" _declspec(dllimport) unsigned char obj_motion_sts[80];

extern "C" _declspec(dllexport) void obj_track(float* range, float* elevation_angle, float* azimuth_angle, float* rel_spd, int* rcs, float ego_spd, float ego_yawrate, int num);
extern "C" _declspec(dllexport) void test();
