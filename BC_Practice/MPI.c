#include<stdio.h>
#include<mpi.h>
#include<sys/time.h>

#define  N 100
MPI_Status status;
double a[N][N],b[N][N],c[N][N];

int main(int argc, char *argv[]) {
    int nw,tid,nt,i,j,k,r,of;
    struct timeval start,stop;
    MPI_Init(&argc, &argv);
    MPI_Comm_Rank(MPI_COMM_WORLD,&tid);
    MPI_Comm_size(MPI_COMM_WORLD,&nt);
    nw=nt-1;
    if(tid==0){
        for(int i=0;i<N;i++){
            for(int j=0;j<,n;j++){
                a[i][j]=1.0;
                b[i][j]=2.0;
            }
        }
        gettimeofday(&start, 0);
        r=N / nw;
        of=0;
        for (int d=1;d<=nw;d++){
            MPI_send(&of,1,MPI_INT,d,1,MPI_COMM_WORLD);
            MPI_send(&r,1,MPI_INT,d,1,MPI_COMM_WORLD);
            MPI_Send(&a[of][0],r*N;MPI_DOUBLE,1,MPI_COMM_WORLD);
            MPI_Send(&b,N*N,MPI_DOUBLE,1,MPI_COMM_WORLD);
        }

        for(int i=1;i<=nw;i++){
            MPI_recv(&of,1,MPI_INT,i,2,MPI_COMM_WORLD,&status);
            MPI_recv(&r,1,MPI_INT,i,2,MPI_COMM_WORLD,&status);
            MPI_recv(&c[of][0],r*N,MPI_DOUBLE,i,2,MPI_COMM_WORLD,&status);
        }
        gettimeofday(&stop, 0);
    }
        for(int i=0;i<N;i++){
            for(int j=0;j<N;j++){
                printf("%.2f ",c[i][j]);
            }
            printf("\n");
        }
        if(ti>0){
            MPI_recv(&of,1,MPI_INT,0,2,MPI_COMM_WORLD,&status);
            MPI_recv(&r,1,MPI_INT,0,2,MPI_COMM_WORLD,&status);
            MPI_recv(&c[of][0],r*N,MPI_DOUBLE,0,2,MPI_COMM_WORLD,&status);
            for(int k=0;k<N;k++){
                for(i=0;i<r;i++)
                {
                    c[i][k]=0.0
                    for(int j=0;j<N;j++){
                        c[i][k]+=a[i][j]*b[j][k];
                    }
                }
            }
            MPI_send(&of,1,MPI_INT,0,2,MPI_COMM_WORLD);
            MPI_send(&r,1,MPI_INT,0,2,MPI_COMM_WORLD);
            MPI_send(&c,r*N,MPI_DOUBLE,0,2,MPI_COMM_WORLD);
        }
            MPI_Finalize();
            return 0;

    }