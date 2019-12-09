#include <stdio.h>
#include "mpi.h"
#include "string.h"
#include <stdlib.h>
#include <time.h>
#include <omp.h>
#include <unistd.h>
//Takayuki Kimura, 28575393, tkim0004@student.monash.edu
#include <arpa/inet.h>
#include <sys/socket.h>
#include <ifaddrs.h>
int basenode( MPI_Comm base_comm, MPI_Comm comm );
int sensor_node( MPI_Comm base_comm, MPI_Comm comm );

void serial_encryption(char msg[]){
    char key[] = "ABC";
    int msgLen = strlen(msg), keyLen = strlen(key), i, j;
 
    char newKey[msgLen], encryptedMsg[msgLen];
    j=0;
    //generating new key
    for(i = 0;i < msgLen;++i){
        j++;
        if(j == keyLen)
            j = 0;
 
        newKey[i] = key[j];
    }
    newKey[i] = '\0';
    
 
    //encryption
    //#pragma omp parallel for
    for(i = 0; i < msgLen; ++i){  
      msg[i] = msg[i] + (newKey[i] - 'A');
      sleep(0.04);
    }
    msg[i] = '\0';

    //return encryptedMsg;
}
void serial_decryption(char msg[]){
    char key[] = "ABC";
    int msgLen = strlen(msg), keyLen = strlen(key), i, j;
 
    char newKey[msgLen], decryptedMsg[msgLen];
    j=0;
    //generating new key
    for(i = 0;i < msgLen;++i){
        j++;
        if(j == keyLen)
            j = 0;
 
        newKey[i] = key[j];
    }
    newKey[i] = '\0';
 
    //decryption
    //#pragma omp parallel for
    for(i = 0; i < msgLen; ++i){
      msg[i] = msg[i] - (newKey[i] - 'A');
      sleep(0.04);
    }
    msg[i] = '\0';

    
}
void encryption(char msg[]){
    char key[] = "ABC";
    int msgLen = strlen(msg), keyLen = strlen(key), i, j;
 
    char newKey[msgLen], encryptedMsg[msgLen];
    j=0;
    //generating new key
    for(i = 0;i < msgLen;++i){
        j++;
        if(j == keyLen)
            j = 0;
 
        newKey[i] = key[j];
    }
    newKey[i] = '\0';
    
 
    //encryption
    #pragma omp parallel for num_threads(2) schedule(dynamic)
    for(i = 0; i < msgLen; ++i){  
      msg[i] = msg[i] + (newKey[i] - 'A');
      sleep(0.04);
    }
    msg[i] = '\0';

    
}

void decryption(char msg[]){
    char key[] = "ABC";
    int msgLen = strlen(msg), keyLen = strlen(key), i, j;
 
    char newKey[msgLen], decryptedMsg[msgLen];
    j=0;
    //generating new key
    for(i = 0;i < msgLen;++i){
        j++;
        if(j == keyLen)
            j = 0;
 
        newKey[i] = key[j];
    }
    newKey[i] = '\0';
 
    //decryption
    #pragma omp parallel for num_threads(2) schedule(dynamic)
    for(i = 0; i < msgLen; ++i){
      msg[i] = msg[i] - (newKey[i] - 'A');
      sleep(0.04);
    }
    msg[i] = '\0';

    
}
//I refer to this website to know how to get IP address https://stackoverflow.com/questions/4139405/how-can-i-get-to-know-the-ip-address-for-interfaces-in-c
void getAddress(char msg[]){
    struct ifaddrs *ifap, *ifa;
    struct sockaddr_in *sa;
    char *addr;
    char buf[256];

    getifaddrs (&ifap);
    for (ifa = ifap; ifa; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr->sa_family==AF_INET) {
            sa = (struct sockaddr_in *) ifa->ifa_addr;
            addr = inet_ntoa(sa->sin_addr);
            snprintf(buf, 256, "IPname is %s Address is %s ", ifa->ifa_name, addr);
            strcat(msg,buf);
	    
        }
    }
    
   
}



int main( argc, argv )
int argc;
char **argv;

{
    int rank, size;
    MPI_Comm new_comm;

    MPI_Init( &argc, &argv );
    MPI_Comm_rank( MPI_COMM_WORLD, &rank );
    MPI_Comm_split( MPI_COMM_WORLD, rank == 0, 0, &new_comm );
    if (rank == 0) {
        basenode( MPI_COMM_WORLD, new_comm );
    }	
    else{
        sensor_node( MPI_COMM_WORLD, new_comm );
    }
	

    MPI_Finalize( );
    return 0;
}







/* base node */
int basenode(MPI_Comm base_comm, MPI_Comm comm )
{
    int        i,j,size,events_per_rank,sum;
    int total_events =0;
    char       message[256*2],date[64];
    char       *tempchar;
    double start_time,end_time,end_commtime,comm_time,enc_time,sp,maxsp,totalMPtime,totalSRtime,totalsp;
    MPI_Status status;
    MPI_Request request;

    MPI_Comm_size( base_comm, &size );
    FILE *fp;
    fp = fopen("log.txt", "wt");
    
    printf("------- basenode has started its computation -------- \n");
    struct ifaddrs *ifap, *ifa;
    struct sockaddr_in *sa;
    char *addr;




    maxsp =0.0;
    for(i=0;i<20;i++){
        events_per_rank = 0;
        MPI_Reduce(&events_per_rank, &sum, 1, MPI_INT, MPI_SUM, 0, base_comm);
        printf("the number of events at iteration %d is %d \n",i,sum);
        total_events+=sum;
        for(j=0;j<sum;j++){
            MPI_Irecv(&message, 256*2, MPI_CHAR, MPI_ANY_SOURCE, MPI_ANY_TAG, base_comm, &request);
            MPI_Wait(&request, &status);
            end_commtime = MPI_Wtime();//measure the end of the communicational time
            //printf("%s",message);

            tempchar = strtok(message,"\n"); //divide the first message
            
            start_time =  MPI_Wtime();//for openmp encryption
            decryption(tempchar);//decrypt actual message
            end_time =  MPI_Wtime();
            comm_time = ((double)(end_time - start_time));
            
            time_t t = time(NULL);
            strftime(date, sizeof(date), "%Y/%m/%d %a %H:%M:%S", localtime(&t));
            fprintf(fp, "time stamp: %s  ", date); // time stamp
            fprintf(fp, "message: %s\r", tempchar);//node number and activation value




            tempchar = strtok(NULL,"\n");   // divide the second message, encryption time
            decryption(tempchar);
            
            enc_time = atof(tempchar);
            fprintf(fp, "encryption time taken is : %f\r\n", enc_time);//encryption time
            fprintf(fp, "decryption time taken is : %f\r\n", comm_time);//decryption time
            totalMPtime = enc_time + comm_time;

            //----------measure the time taken by serial encryption and decryption ----------
            start_time =  MPI_Wtime();
            serial_encryption(message);
            end_time =  MPI_Wtime();
            enc_time = ((double)(end_time - start_time)); //time taken for serial encryption
            fprintf(fp, "serial encryption time taken is : %f\r\n", enc_time);//encryption time

            start_time =  MPI_Wtime();
            serial_decryption(message);
            end_time =  MPI_Wtime();
            comm_time = ((double)(end_time - start_time)); //time taken for serial encryption
            fprintf(fp, "serial decryption time taken is : %f\r\n", comm_time);//decryption time

            totalSRtime = enc_time + comm_time;

            sp = totalSRtime / totalMPtime; //calculate speed up
            totalsp +=sp;
            fprintf(fp, "the speed up is : %f\r\n", sp);
            if(maxsp <sp){
                maxsp = sp;     
            }
            



            tempchar = strtok(NULL,"\n");   // divide the third message,  start time of Isend
            start_time = atof(tempchar);
            comm_time = ((double)(end_commtime - start_time));
            fprintf(fp,"communicational time taken is : %f  \n", comm_time);//communicational time taken between sensor node and base node
            
    
            
            
        }
	}
    fprintf(fp, "the total number of events during the computation is %d\r\n", total_events);//summary of communication,summary of activations
    fprintf(fp,"the average speed up is : %f  \n", totalsp / total_events);
    fprintf(fp,"the maximum speed up is : %f  \n", maxsp);
    fprintf(fp, "This is the end of the text");
    fclose(fp);
    printf("------- basenode has finished its computation ------- \n");
    
}

/* sensor nodes */
int sensor_node(MPI_Comm base_comm, MPI_Comm comm )
{
    
    int  i,j,sensor_rank, randvalue,value;
    int events_per_rank,sum; //for mpi reduce
    char message[256*2];
    double start_time,end_time,comm_time; //for measuring time
    char buf[256];      // for converting double to char
    

    MPI_Status status;
    MPI_Request request;
    //MPI_Comm_size( comm, &size );
    MPI_Comm_rank( comm, &sensor_rank );
    MPI_Comm commfor2dims;
    int numberOfdims,dimsize[2], joint[2],reorder;
    int coordinates[2],UpNode,DownNode,LeftNode,RightNode;
    
    numberOfdims =2; //the number of dimentions
    dimsize[0]=4; //height of matrix
    dimsize[1]=5; //width of matrix
    joint[0] = 0; //false, not connected to the node in opposite side in col
    joint[1] = 0; //false  not connected to the node in opposite side in row
    reorder = 0;

    //create new comminicator with new cartesian topology
    MPI_Cart_create(comm, numberOfdims, dimsize, joint,reorder, &commfor2dims);
    //obtain coordinates of the given rank
    MPI_Cart_coords(commfor2dims,sensor_rank,2,coordinates);
    //get adjacent nodes, second input is direction, third input is distance
    MPI_Cart_shift(commfor2dims,0,1,&UpNode,&DownNode);
    MPI_Cart_shift(commfor2dims,1,1,&LeftNode,&RightNode);

    printf("-------- rank %d has Upnode %d DownNode %d LeftNode %d RightNode %d --------- \n",sensor_rank,UpNode,DownNode,LeftNode,RightNode);
    
    
    //int array[4] = {-1, -1, -1, -1};
    //sliding window method, the size is 3
    int array[][3] = {{-1, -1, -1},{-1, -1, -1},{-1, -1, -1},{-1, -1, -1}};
    
    int lower =0;
    int upper =9;
    int counting_array[10][2]={};//used for counting sort, 0 to 19

    int adjacent_array[4] ={};
    adjacent_array[0] = UpNode;
    adjacent_array[1] = DownNode;
    adjacent_array[2] = LeftNode;
    adjacent_array[3] = RightNode; 

    
    int adjacentnum,counter,window_row,window_col,activation_num;
    char date[64];
    time_t t = time(NULL);

    //printf("-------- %d has started its computation -------\n",sensor_rank);
    for(i=0;i<20;i++){
        events_per_rank = 0;


        srand((unsigned int)time(NULL));
        randvalue=rand() % upper + lower;
        srand(sensor_rank + i + randvalue);
        randvalue=rand() % upper + lower;
        srand(sensor_rank + i + randvalue);
        randvalue=rand() % upper + lower;
        //printf("node %d i= %d before enc %d\n",sensor_rank,i,randvalue);
        snprintf(buf, 256, "%d", randvalue);//convert int to string
        encryption(buf); //encrypt randvalue
        //printf("node %d i= %d encrypted %s\n",sensor_rank,i,buf);

        //printf("rank %d has randvalue %d at iteration %d \n",sensor_rank,randvalue,i);
        //-------Send the random value to adjacnet nodes ---------------
        for(j=0;j<4;j++){
            if(adjacent_array[j]>=0){
                
                MPI_Isend( &buf, 256, MPI_CHAR, adjacent_array[j], i, comm, &request);
                
            }
        }
        //----------Receive the random value from adjacent nodes --------------
        for(j=0;j<4;j++){
            if(adjacent_array[j]>=0){
                MPI_Irecv(&buf, 256, MPI_CHAR, adjacent_array[j], i, comm, &request);
                //could be MPI_ANY_TAG
                MPI_Wait(&request, &status);
                decryption(buf);
                //printf("node %d i= %d decrypted %s\n",sensor_rank,i,buf);
                value = atof(buf);//convert string to int
                //printf("node %d i= %d decrypted %d\n",sensor_rank,i,value);

                if(i==0){
                    array[j][0] =value;
                    //printf("this is i=0 %d\n",value);
                    
                }
                if(i==1){
                    array[j][1] = value;
                }
                if(i>1){
                    array[j][2] = value;
                }
            }
        }

      

        
        //apply counting sort concept
        for(window_row=0;window_row<4;window_row++){
            for(window_col=0;window_col<3;window_col++){
                value = array[window_row][window_col];
                if(value >= lower && value <=upper ){
                   // printf("counting array value %d is count %d at i=%d \n",value,counting_array[value][0],i);

                    // if same value appears in same node, it should not be counted since only same value in different node is considered as an event
                    // counting_array[][1] is a checker, if 0, first occurrence, if 1, it is repeated number and ignore it
                    if(counting_array[value][1]<1){

                        counting_array[value][0]+=1;
                        counting_array[value][1] =1;
                    }
                }
            }
            // reset the checker used to avoid repeating before moving to the next node values
            for(window_col=0;window_col<3;window_col++){
                value = array[window_row][window_col];
                counting_array[value][1] =0;
            }

        
        }

        activation_num =-1;
        
        for(j=0;j<upper+1;j++){
            //printf("number is %d value is %d",j,counting_array[j]);
            //printf("\n");
            if(counting_array[j][0] > 2){
                activation_num = j;
            }

        }
        
        

      

        /*printf("%d received all values at iteration %d \n",sensor_rank,i);
        for(j=0;j<adjacentnum;j++){
                printf("%d ",array[j]);
        }
        printf("\n");*/

        //if there is activation, report to base node
        if(activation_num>=0){
            
            
            strftime(date, sizeof(date), "%Y/%m/%d %a %H:%M:%S", localtime(&t));
            printf("%s\n", date);
        
            printf("sensor node %d activated an event with value %d at iteration %d \n",sensor_rank,activation_num,i);
            for(window_row=0;window_row<4;window_row++){
                for(window_col=0;window_col<3;window_col++){
                    if(window_col<2){
                        printf("%d ",array[window_row][window_col]);
                    }
                    else{
                        printf("%d \n",array[window_row][window_col]);
                    }

                }
                
            }
            printf("\n");

            
            
            
            sprintf( message, "sensor node %d activated an event with value %d at iteration %d ",sensor_rank,activation_num,i );
            getAddress(message);//concatinate a message with IP address
            
            
            //-----------measure cipher time------------------  
            
            
            
            

            //encryption is here
            //for openmp encryption
        
            start_time =  MPI_Wtime();
            encryption(message);
            
            //printf("encrypted is %s\n",message);
            end_time =  MPI_Wtime();
            comm_time = ((double)(end_time - start_time)); //time taken for openmp encryption
            //printf("Rank %d at i = %d OpenMP encryption time: %lf\n",sensor_rank,i, comm_time);

          
            //encrypt time taken by message encryption
            snprintf(buf, 256, "%f", comm_time); //convert double to string
            encryption(buf);
            //printf("Rank %d at i = %d encrypted encryption time: %s\n",sensor_rank,i, buf);
            strcat(message, "\n");
            strcat(message, buf);//combine message string with encryption time
            strcat(message, "\n");

            start_time =  MPI_Wtime();//communicational time between sensor node and base node
            //printf("Rank %d at i = %d comm time: %lf\n",sensor_rank,i, start_time);
            snprintf(buf, 256, "%f", start_time);
            //printf("Rank %d at i = %d comm time: %s\n",sensor_rank,i, buf);
            strcat(message, buf);//combine the message with communicational time 
            //printf("before Isend %s\n",message);
            MPI_Isend( message, 256*2, MPI_CHAR, 0, 0, base_comm, &request);
            events_per_rank =1;
            
        }

        //slide the window
        for(window_col=0;window_col<2;window_col++){
            for(window_row=0;window_row<4;window_row++){
                array[window_row][window_col] =array[window_row][window_col+1]; 
            }
        }

        //reset counting array
        for(j=0;j< upper+1;j++){
            counting_array[j][0] =0;
        }
        MPI_Reduce(&events_per_rank, &sum, 1, MPI_INT, MPI_SUM, 0, base_comm);
        



    }

    //printf("------ %d has ended its computation -----\n",sensor_rank);
    
    
    

    return 0;
}
