//////////////////////////////////////////////////////////////////////////////////////
// mandelbrot.c program: Mandelbort Set Fractal (Color Serial Code Implementation).
// --------------------------------
//  1. Draws Mandelbrot set for Fc(z) = z*z +c
//  using Mandelbrot algorithm ( boolean escape time )
//	This code is modified from the original version as available at:
//	http://rosettacode.org/wiki/Mandelbrot_set#PPM_non_interactive
// -------------------------------         
// 2. Technique of creating ppm file is  based on the code of Claudio Rocchini
// http://en.wikipedia.org/wiki/Image:Color_complex_plot.jpg
// create 24 bit color graphic file ,  portable pixmap file = PPM 
// see http://en.wikipedia.org/wiki/Portable_pixmap
// to see the file use external application ( graphic viewer)
//////////////////////////////////////////////////////////////////////////////////////
//Takayuki Kimura, 28575393, tkim0004@student.monash.edu
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <mpi.h>

// Main program
int main(int argc, char** argv)
 {  double overall =  MPI_Wtime();
	/* screen ( integer) coordinate */
	int iX,iY;
	const int iXmax = 8000; // default
	const int iYmax = 8000; // default

	/* world ( double) coordinate = parameter plane*/
	double Cx, Cy;
	const double CxMin = -2.5;
	const double CxMax = 1.5;
	const double CyMin = -2.0;
	const double CyMax = 2.0;

	/* */
	double PixelWidth = (CxMax - CxMin)/iXmax;
	double PixelHeight = (CyMax - CyMin)/iYmax;

	/* color component ( R or G or B) is coded from 0 to 255 */
	/* it is 24 bit color RGB file */
	const int MaxColorComponentValue = 255; 
	FILE * fp;
	char *filename = "Mandelbrot.ppm";
	char *comment = "# ";	/* comment should start with # */

	// RGB color array
	static unsigned char color[3];


	

	/* Z = Zx + Zy*i;	Z0 = 0 */
	double Zx, Zy;
	double Zx2, Zy2; /* Zx2 = Zx*Zx;  Zy2 = Zy*Zy  */
	/*  */
	int Iteration;
	const int IterationMax = 2000; // default

	/* bail-out value , radius of circle ;  */
	const double EscapeRadius = 400;
	double ER2 = EscapeRadius * EscapeRadius;
	
	/* Clock information */
	double start, end;
	double cpu_time_used;

	// MPI declaration 

	MPI_Init(&argc, &argv);
	MPI_Request request;
	MPI_Status stat;
	int rank, processors;
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &processors);
    if(rank ==0){
		/*create new file,give it a name and open it in binary mode  */
		fp = fopen(filename, "wb"); /* b -  binary mode */

		/*write ASCII header to the file (PPM file format)*/
		fprintf(fp,"P6\n %s\n %d\n %d\n %d\n", comment, iXmax, iYmax, MaxColorComponentValue);

		printf("File: %s successfully opened for writing.\n", filename);
		printf("Computing Mandelbrot Set. Please wait...\n");

		// Get current clock time.
		start =  MPI_Wtime();
	}

	// -----------------my part ---------------------
	int i;
	int oddcheck = processors %2;
	int division;
	if (oddcheck ==0){
		division = processors / 2; //what IX will be divided by 
	}
	else{
		division = (processors+1) /2;
		processors+=1;
	}


	//int iY_per_procs = iYmax / 2;
	int iX_per_procs = iXmax / division; 
	int iX_remain = iXmax % division;
    
    unsigned char *temp = (unsigned char*)calloc( iYmax * (iXmax) * 3 , sizeof(unsigned char));
	
	
	
	/*if(rank== (processors/2)-1 || rank == processors-1){
		unsigned char temp[(iX_per_procs+iX_remain)*3];
	}else{

		if(rank==0 && oddcheck!=0){
			unsigned char temp[(iX_per_procs+iX_remain)*3];

		}
		unsigned char temp[iX_per_procs*3]
	}*/
	
	int index=0;

    int startY,endY,startX,endX;

	if(rank < (processors/2)){ //if the processor deal with the above half on Y axis
		startY = 0; 
		endY = iYmax/2;
		
	}else{ //if processor deal with the below half on Y axis
		startY = iYmax/2;
		endY = iYmax;
	}

	if(rank < processors/2){
		if(rank==processors/2-1){ //if the processor is the one dealing with the remainder part
			startX = rank*iX_per_procs;
			endX =  startX + iX_per_procs + iX_remain;
		}else{
			startX = rank * iX_per_procs;
			endX =  startX + iX_per_procs;
		}
	}else{
		if(rank == processors-1){ //if the processor is the one dealing with the remainder part
			startX = (rank - processors/2)*iX_per_procs;
			endX = startX + iX_per_procs + iX_remain;
		}else{
			startX = (rank - processors/2)*iX_per_procs;
			endX = startX + iX_per_procs;
		}
	}

	
    unsigned char *firstarr;
	if(rank==0){firstarr = (unsigned char*)calloc( (endY-startY) * (iXmax) * 3 , sizeof(unsigned char));}
    
    if(rank ==0){
        index =0;
		for(iY = startY; iY <endY; iY++){
			Cy = CyMin + (iY * PixelHeight);
			if (fabs(Cy) < (PixelHeight / 2))
			{
				Cy = 0.0; /* Main antenna */
			}

			for(iX = startX; iX < endX; iX++)
			{
				Cx = CxMin + (iX * PixelWidth);
				/* initial value of orbit = critical point Z= 0 */
				Zx = 0.0;
				Zy = 0.0;
				Zx2 = Zx * Zx;
				Zy2 = Zy * Zy;

					/* */
				for(Iteration = 0; Iteration < IterationMax && ((Zx2 + Zy2) < ER2); Iteration++)
				{
					Zy = (2 * Zx * Zy) + Cy;
					Zx = Zx2 - Zy2 + Cx;
					Zx2 = Zx * Zx;
					Zy2 = Zy * Zy;
				};

					/* compute  pixel color (24 bit = 3 bytes) */
				if (Iteration == IterationMax)
				{
					// Point within the set. Mark it as black
					color[0] = 0;
					color[1] = 0;
					color[2] = 0;
				}
				else 
				{
					// Point outside the set. Mark it as white
					double c = 3*log((double)Iteration)/log((double)(IterationMax) - 1.0);
					if (c < 1)
					{
						color[0] = 0;
						color[1] = 0;
						color[2] = 255*c;
					}
					else if (c < 2)
					{
						color[0] = 0;
						color[1] = 255*(c-1);
						color[2] = 255;
					}
					else
					{
						color[0] = 255*(c-2);
						color[1] = 255;
						color[2] = 255;
					}
				}
				//fwrite(color,1,3,fp);
				firstarr[index]=color[0];
				firstarr[index+1]= color[1];
				firstarr[index+2]= color[2];
				index+=3;
			}
		}
		index =0;
		




        //printf("remainder is %d .\n",iX_remain);
        int i;
        int result_offset=0;
		int loopcount =processors;
		if(oddcheck!=0){
			loopcount-=1;
		}
        for(i=1;i<loopcount;i++){
            
            //printf("rank %d offset is%d.\n",i,result_offset);
            if(i==processors/2-1 ||i==processors-1){
                //printf("recv remainder i is %d offset is %d.\n",i,result_offset);
                MPI_Recv(temp+result_offset,(endY - startY) * (iX_per_procs+iX_remain)* 3, MPI_UNSIGNED_CHAR, i, 0, MPI_COMM_WORLD, &stat);
                result_offset += (endY - startY) * (iX_per_procs+iX_remain)* 3;
                //printf("rank %d received.\n",i);

            }else{
                //printf("recv i is %d offset is %d.\n",i,result_offset);
                MPI_Recv(temp+result_offset,(endY - startY) * (iX_per_procs)*3 , MPI_UNSIGNED_CHAR, i, 0, MPI_COMM_WORLD, &stat);
                result_offset += (endY - startY) * (iX_per_procs)* 3;
                //printf("rank %d received.\n",i);
            }
            
            
        }
    }


    
    
	if(rank == 0){
        
        
		

		/* compute and write image data bytes to the file */
		//IYmax, IXmax are 8000 default
        
        //printf("rank %d startY is %d and endY is %d.\n",rank,startY,endY);
		//printf("rank %d startX is %d and endX is %d.\n",rank,startX,endX);
		

		
				
		
		       
	    
		for(iY = startY; iY <endY; iY++){
			fwrite(firstarr +(iY*(iX_per_procs)*3),1,(iX_per_procs)*3,fp);
			
			for(i=0;i<(processors/2)-1;i++){
                if(i==processors/2-2){
                    
                    fwrite(temp+(i*((endY-startY)*(iX_per_procs)*3))+(iY*(iX_per_procs+iX_remain)*3),1,(iX_per_procs+iX_remain)*3,fp);
                    //(endY - startY) * (iX_per_procs+iX_remain)* 3
                }else{
                    
                    fwrite(temp+(i*((endY-startY)*iX_per_procs*3))+(iY*(iX_per_procs)*3),1,(iX_per_procs)*3,fp);
                }
			    
			}
		}
        
		//printf("process 0 and 1 successfully called fwrite.\n");
		for(iY = endY; iY < iYmax; iY++){
			
			for(i=(processors/2)-1;i<processors-1;i++){
                if(i==processors-2){
					if(oddcheck!=0){
						startX = ((processors-1) - processors/2)*iX_per_procs;
			            endX = startX + iX_per_procs + iX_remain;

						Cy = CyMin + (iY * PixelHeight);
						index =0;
						if (fabs(Cy) < (PixelHeight / 2))
						{
							Cy = 0.0; /* Main antenna */
						}

						for(iX = startX; iX < endX; iX++)
						{
							Cx = CxMin + (iX * PixelWidth);
							/* initial value of orbit = critical point Z= 0 */
							Zx = 0.0;
							Zy = 0.0;
							Zx2 = Zx * Zx;
							Zy2 = Zy * Zy;

								/* */
							for(Iteration = 0; Iteration < IterationMax && ((Zx2 + Zy2) < ER2); Iteration++)
							{
								Zy = (2 * Zx * Zy) + Cy;
								Zx = Zx2 - Zy2 + Cx;
								Zx2 = Zx * Zx;
								Zy2 = Zy * Zy;
							};

								/* compute  pixel color (24 bit = 3 bytes) */
							if (Iteration == IterationMax)
							{
								// Point within the set. Mark it as black
								color[0] = 0;
								color[1] = 0;
								color[2] = 0;
							}
							else 
							{
								// Point outside the set. Mark it as white
								double c = 3*log((double)Iteration)/log((double)(IterationMax) - 1.0);
								if (c < 1)
								{
									color[0] = 0;
									color[1] = 0;
									color[2] = 255*c;
								}
								else if (c < 2)
								{
									color[0] = 0;
									color[1] = 255*(c-1);
									color[2] = 255;
								}
								else
								{
									color[0] = 255*(c-2);
									color[1] = 255;
									color[2] = 255;
								}
							}
							fwrite(color,1,3,fp);
						}

					}else{
						fwrite(temp+((i-1)*((endY-startY)*iX_per_procs*3)) + ((endY-startY)*(iX_per_procs+iX_remain)*3) +((iY-endY)*(iX_per_procs+iX_remain)*3),1,(iX_per_procs+iX_remain)*3,fp);
					}
                    
                    
                    //(endY - startY) * (iX_per_procs+iX_remain)* 3
                }else{
                    
                    fwrite(temp+   ((i-1)*((endY-startY)*iX_per_procs*3)) + ((endY-startY)*(iX_per_procs+iX_remain)*3) + ((iY-endY)*(iX_per_procs)*3),1,(iX_per_procs)*3,fp);
                }
			}
		}
		//printf("process 2 and 3 successfully received.\n");
	
			
		
		
	}else{
		
		
        printf("rank %d successfully started.\n",rank);
		/* compute and write image data bytes to the file */
		//IYmax, IXmax are 8000 default
		printf("rank %d startY is %d and endY is %d.\n",rank,startY,endY);
		printf("rank %d startX is %d and endX is %d.\n",rank,startX,endX);
		for(iY = startY; iY < endY; iY++)
		{
			
			Cy = CyMin + (iY * PixelHeight);
			if (fabs(Cy) < (PixelHeight / 2))
			{
				Cy = 0.0; /* Main antenna */
			}

			for(iX = startX; iX < endX; iX++)
			{
				Cx = CxMin + (iX * PixelWidth);
				/* initial value of orbit = critical point Z= 0 */
				Zx = 0.0;
				Zy = 0.0;
				Zx2 = Zx * Zx;
				Zy2 = Zy * Zy;

				/* */
				for(Iteration = 0; Iteration < IterationMax && ((Zx2 + Zy2) < ER2); Iteration++)
				{
					Zy = (2 * Zx * Zy) + Cy;
					Zx = Zx2 - Zy2 + Cx;
					Zx2 = Zx * Zx;
					Zy2 = Zy * Zy;
				};

				/* compute  pixel color (24 bit = 3 bytes) */
				if (Iteration == IterationMax)
				{
					// Point within the set. Mark it as black
					color[0] = 0;
					color[1] = 0;
					color[2] = 0;
				}
				else 
				{
					// Point outside the set. Mark it as white
					double c = 3*log((double)Iteration)/log((double)(IterationMax) - 1.0);
					if (c < 1)
					{
						color[0] = 0;
						color[1] = 0;
						color[2] = 255*c;
					}
					else if (c < 2)
					{
						color[0] = 0;
						color[1] = 255*(c-1);
						color[2] = 255;
					}
					else
					{
						color[0] = 255*(c-2);
						color[1] = 255;
						color[2] = 255;
					}
				}
				temp[index]=color[0];
				temp[index+1]= color[1];
				temp[index+2]= color[2];
				index+=3;
				//fwrite(color, 1, 3, fp);
				
				
				
			}

		}
        
        if(rank==processors/2-1 || rank ==processors-1){
            //printf("remainder process %d successfully send %d.\n",rank,processors/2-1);
            MPI_Send(temp,(endY-startY) * (iX_per_procs+iX_remain)*3 , MPI_UNSIGNED_CHAR, 0, 0, MPI_COMM_WORLD);
        }else{
            //printf("process %d successfully send.\n",rank);
            MPI_Send(temp,(endY-startY) * (iX_per_procs)*3 , MPI_UNSIGNED_CHAR, 0, 0, MPI_COMM_WORLD);
        }
		//MPI_Wait(&request,&stat);
		
	}
	// Get the clock current time again
	// Subtract end from start to get the CPU time used.
	
	if(rank ==0){
		//printf("process 0 ending time.\n");
		end = MPI_Wtime();
		cpu_time_used = ((double)(end - start)) ;

		fclose(fp);

		printf("Completed Computing Mandelbrot Set.\n");
		printf("File: %s successfully closed.\n", filename);
		printf("Mandelbrot computational process time: %lf\n", cpu_time_used);
		end = MPI_Wtime();
		cpu_time_used = ((double)(end - overall)) ;
		printf("Mandelbrot overall time: %lf\n", cpu_time_used);
        
	}
	//printf("process %d successfully finish execution.\n",rank);
    MPI_Finalize();
	return 0;
}

