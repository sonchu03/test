#include<stdio.h>
#include<time.h>
#include<string.h>
struct date
{
    int ngay;
    int thang;
    int nam;
};
struct sinhvien
{
    int id;
    char ten[100];
    char gioitinh[5];
    date ngaysinh;
    int tuoi;
    float diemmon1;
    float diemmon2;
    float diemmon3;
    float diemtrungbinh;
    char hocluc[10];
    char malop[30];
};
void xoaxuongdong(char x[]){
    size_t len = strlen(x);
    if(x[len-1] == '\n'){
        x[len-1]='\0';
    }
}
typedef sinhvien SV;
void nhapsinhvien(SV &sv){
    printf("\nID ");
    scanf("%d",&sv.id);
    printf("\nten ");
    fflush(stdin);
    fgets(sv.ten,sizeof(sv.ten),stdin);
    xoaxuongdong(sv.ten);
    printf("\ngioi tinh ");
    fflush(stdin);
    fgets(sv.gioitinh,sizeof(sv.gioitinh),stdin);
    xoaxuongdong(sv.gioitinh);
    printf("\nngay sinh ");
    scanf("%d%d%d",&sv.ngaysinh.ngay,&sv.ngaysinh.thang,&sv.ngaysinh.nam);
    printf("\ndiem mon 1 la ");scanf("%f",&sv.diemmon1);
    printf("\ndiem mon 2 la ");scanf("%f",&sv.diemmon2);
    printf("\ndiem mon 3 la ");scanf("%f",&sv.diemmon3);
    printf("\nma lop la ");
    fflush(stdin);
    fgets(sv.malop,sizeof(sv.malop),stdin);
    xoaxuongdong(sv.malop);

}
void tinhtuoicuahocsinh(SV &sv){
    time_t TTIME = time(0);
    tm* NOW = localtime(&TTIME);
    int namhientai = NOW->tm_year+1900;
    sv.tuoi = namhientai - sv.ngaysinh.nam;
}
void insinhvien(SV sv){
    printf("%d \t %s \t %s\t %d/%d/%d \t %d \t %.2f \t %.2f \t %.2f\t %f\t %s\t %s\t",sv.id,sv.ten,sv.gioitinh,sv.ngaysinh.ngay,sv.ngaysinh.thang,sv.ngaysinh.nam,sv.tuoi,sv.diemmon1,sv.diemmon2,sv.diemmon3,sv.diemtrungbinh,sv.hocluc,sv.malop);
}
void tinhdiemtrungbinh(SV *sv){
    sv->diemtrungbinh = (sv->diemmon1+sv->diemmon2+sv->diemmon3)/3;
}
void xeploai(SV &sv){
    if(sv.diemtrungbinh > 8){
        strcpy(sv.hocluc,"gioi");
    }else if(sv.diemtrungbinh > 6){
        strcpy(sv.hocluc,"kha");
    }else (sv.diemtrungbinh > 4);{
        strcpy(sv.hocluc,"kem");
    }
}
void capnhatsinhvien(SV &sv){
    nhapsinhvien(sv);
    tinhtuoicuahocsinh(sv);
    tinhdiemtrungbinh(&sv);
    xeploai(sv);
}
int main(){
    SV sv1;
    capnhatsinhvien(sv1);
    tinhtuoicuahocsinh(sv1);
    tinhdiemtrungbinh(&sv1);
    xeploai(sv1);
    insinhvien(sv1);
}
//sonchudaoday//
//dafuyadfva//
//daoday//
