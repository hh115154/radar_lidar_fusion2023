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
extern "C" _declspec(dllimport) unsigned char obj_id_outp[10];
extern "C" _declspec(dllimport) unsigned char obj_typ_outp[10];
extern "C" _declspec(dllimport) float obj_px_outp[10];
extern "C" _declspec(dllimport) float obj_py_outp[10];
extern "C" _declspec(dllimport) float obj_pz_outp[10];
extern "C" _declspec(dllimport) float obj_vx_outp[10];
extern "C" _declspec(dllimport) float obj_vy_outp[10];
extern "C" _declspec(dllimport) float obj_vz_outp[10];
extern "C" _declspec(dllimport) float obj_length_outp[10];
extern "C" _declspec(dllimport) float obj_width_outp[10];
extern "C" _declspec(dllimport) float obj_heigth_outp[10];

extern "C" _declspec(dllexport) void obj_track(float* px, float* py, float* pz, float* rel_spd, int* rcs, float ego_spd, float ego_yawrate, int num);

