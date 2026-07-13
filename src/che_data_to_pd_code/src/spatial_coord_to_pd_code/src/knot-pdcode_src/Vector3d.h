#pragma once

#include <cstdio>
#include <cmath>

#ifndef M_PI // 定义圆周率
#define M_PI (3.14159265358979323846)
#endif

struct Vector2d {
    double x[2];

    Vector2d(double pX, double pY) {
        this->getX() = pX;
        this->getY() = pY;
    }

    double& getX() {return x[0];}
    double& getY() {return x[1];}

    double getX() const {return x[0];}
    double getY() const {return x[1];}

    double getLength() const { // 计算向量模长
        return sqrt(SQR(getX()) + SQR(getY()));
    }
    
    void multiply(double p) { // 数乘向量
        getX() *= p;
        getY() *= p;
    }

    void add(const Vector2d& vector_2d) { // 向量加法
        this->getX() += vector_2d.getX();
        this->getY() += vector_2d.getY();
    }
    
    void sub(const Vector2d& vector_2d) { // 向量减法
        this->getX() -= vector_2d.getX();
        this->getY() -= vector_2d.getY();
    }

    double dot(const Vector2d& vector_2d) { // 向量点乘
        return 
            (this->getX() * vector_2d.getX() +
             this->getY() * vector_2d.getY());
    }

    void unify() {
        if(this->getLength() > 0) { // 只对非零向量做单位化
            this->multiply(1.0 / this->getLength());
        }
    }

    static double cross(const Vector2d& v1, const Vector2d& v2) { // 二维叉积
        double x1 = v1.getX(), y1 = v1.getY();
        double x2 = v2.getX(), y2 = v2.getY();

        return x1*y2 - x2*y1;
    }

    double calculateAngle() const {
        double angle = std::atan2(this->getY(), this->getX());
        if (angle < 0) {
            angle += 2 * M_PI;
        }
        return angle;
    }

    void debugOutput() const { // 输出点坐标
        double pX, pY;
        pX = this->getX();
        pY = this->getY();

        printf("%25.17lf %25.17lf\n", pX, pY);
    }

private:
    static double SQR(double x) {return x * x;}
};

struct Vector3d { // 三维空间中的点
    double x[3];

    Vector3d(double pX, double pY, double pZ) {
        this->getX() = pX;
        this->getY() = pY;
        this->getZ() = pZ;
    }
    
    Vector2d getVector2d() const { // 裁剪掉第三维度
        return Vector2d(this->getX(), this->getY());
    }

    double& getX() {return x[0];}
    double& getY() {return x[1];}
    double& getZ() {return x[2];}

    double getX() const {return x[0];}
    double getY() const {return x[1];}
    double getZ() const {return x[2];}

    double getLength() const { // 计算向量模长
        return sqrt(SQR(getX()) + SQR(getY()) + SQR(getZ()));
    }

    void multiply(double p) { // 数乘向量
        getX() *= p;
        getY() *= p;
        getZ() *= p;
    }

    void add(const Vector3d& vector_3d) { // 向量加法
        this->getX() += vector_3d.getX();
        this->getY() += vector_3d.getY();
        this->getZ() += vector_3d.getZ();
    }
    
    void sub(const Vector3d& vector_3d) { // 向量减法
        this->getX() -= vector_3d.getX();
        this->getY() -= vector_3d.getY();
        this->getZ() -= vector_3d.getZ();
    }

    double dot(const Vector3d& vector_3d) { // 向量点乘
        return 
            (this->getX() * vector_3d.getX() +
             this->getY() * vector_3d.getY() +
             this->getZ() * vector_3d.getZ());
    }

    void unify() {
        if(this->getLength() > 0) { // 只对非零向量做单位化
            this->multiply(1.0 / this->getLength());
        }
    }

    static Vector3d cross(const Vector3d& v1, const Vector3d& v2) { // 向量叉积
        double x1 = v1.getX(), y1 = v1.getY(), z1 = v1.getZ();
        double x2 = v2.getX(), y2 = v2.getY(), z2 = v2.getZ();

        return Vector3d(
             (y1*z2 - y2*z1),
            -(x1*z2 - x2*z1),
             (x1*y2 - x2*y1) // 计算向量叉积
        );
    }

    void debugOutput() const { // 输出点坐标
        double pX, pY, pZ;
        pX = this->getX();
        pY = this->getY();
        pZ = this->getZ();

        printf("%25.17lf %25.17lf %25.17lf\n", pX, pY, pZ);
    }

private:
    static double SQR(double x) {return x * x;}
};