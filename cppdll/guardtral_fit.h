#pragma once

#include"pch.h"
#include <vector>
#include<Eigen/Dense>
using namespace std;
using namespace Eigen;

typedef unsigned char uint8_t;

class point
{
public:
    point():px(0),py(0),pz(0),rcs(0){};
    float px;
    float py;
    float pz;
    int rcs;
};



class guardtral{
public:
    guardtral(uint8_t order,uint8_t num,vector<float> fac_):orders(order),points_num_lim(num),fac(fac_),init_flg(0){
        X.resize(order);
        Y.resize(order);
        coef_cur.resize(order+1);
        coef.resize(order+1);
        coef_lst.resize(order+1);
        fac.resize(fac_.size());
        fac = fac_;


    }
    guardtral(const guardtral& guard){
        this->X = guard.X;
        this->Y = guard.Y;
        this->orders = guard.orders;
        this->coef = guard.coef;
        this->coef_lst = guard.coef_lst;
        this->points_num_lim = guard.points_num_lim;

    }
    void set_X(vector<float> x);
    void set_Y(vector<float> y);
    void set_orders(uint8_t orders);
    Eigen::VectorXf get_coef();
    void set_fac(vector<float> fac_){fac = fac_;}
    void FitterLeastSquareMethod(vector<float> point_x,vector<float> point_y);
    void fit_init(vector<float> point_x,vector<float> point_y);
    void guardtralfit(vector<float> point_x,vector<float> point_y);
private:
    std::vector<float> X;
    std::vector<float> Y;
    uint8_t orders;
    Eigen::VectorXf coef;
    Eigen::VectorXf coef_cur;
    Eigen::VectorXf coef_lst;
    uint8_t points_num_lim;
    std::vector<float> fac;
    bool init_flg;
};

extern "C" _declspec(dllexport) float* get_guardtral(float* x, float* y, float* z, int* rcs, int num);
