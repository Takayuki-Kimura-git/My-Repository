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

    int startvalue,endvalue;
	int screen_per_procs,screen_remain;
	
	

	screen_per_procs = iYmax / processors;
	screen_remain = iYmax % processors;
		
	//screen_per_procs = iYmax / processors;
	
	
	unsigned char *temp = (unsigned char*)calloc( (screen_per_procs + screen_remain) * iXmax * 3 , sizeof(unsigned char));
	
	
	int index=0;
    
	if(rank == 0){
		screen_per_procs = iYmax / processors;
		screen_remain = iYmax % processors;
	    startvalue = rank * screen_per_procs;
	    endvalue = startvalue + screen_per_procs + screen_remain;

		/* compute and write image data bytes to the file */
		//IYmax, IXmax are 8000 default
		for(iY = startvalue; iY < endvalue; iY++)
		{
			Cy = CyMin + (iY * PixelHeight);
			if (fabs(Cy) < (PixelHeight / 2))
			{
				Cy = 0.0; /* Main antenna */
			}

			for(iX = 0; iX < iXmax; iX++)
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
		fwrite(temp, 1, (screen_per_procs+screen_remain) * iXmax * 3, fp);
		//fwrite(&temp,1, screen_per_procs*iXmax*3,fp);
		//printf("process %d successfully completed.\n",0);		
		
		int i;
		for(i=1; i<processors; i++){
			//printf("i is %d will receive\n", i);
			MPI_Recv(temp,screen_per_procs * iXmax * 3, MPI_UNSIGNED_CHAR, i, 0, MPI_COMM_WORLD, &stat);
			fwrite(temp,1,screen_per_procs * iXmax * 3,fp);
			
			
		
	        /*
			if(i == processors-1){
				startvalue = i * screen_per_procs;
				screen_remain = iYmax % processors;
	            endvalue = startvalue + screen_per_procs + screen_remain;
				for(iY = startvalue; iY < endvalue; iY++){
					MPI_Recv(temp, iXmax*3, MPI_UNSIGNED_CHAR, i, 0, MPI_COMM_WORLD, &stat);
				    fwrite(temp,1,iXmax*3,fp);
				}
			}else{
				startvalue = i * screen_per_procs;
	            endvalue = startvalue + screen_per_procs;
				for(iY = startvalue; iY < endvalue; iY++){
					MPI_Recv(temp, iXmax*3, MPI_UNSIGNED_CHAR, i, 0, MPI_COMM_WORLD, &stat);
					//printf("iY is %d iX is %d\n", iY,iX);
				    fwrite(temp,1,iXmax*3,fp);
				}

				
			}*/
			
			//printf("process %d successfully received.\n",i);
			
		}
		
	}else{
		screen_per_procs = iYmax / processors;
		screen_remain = iYmax % processors;
		startvalue = (rank * screen_per_procs)+screen_remain;
		endvalue = startvalue + screen_per_procs;
		
		
        //printf("process %d successfully started.\n",rank);
		/* compute and write image data bytes to the file */
		//IYmax, IXmax are 8000 default
		//printf("process %d and %d.\n",startvalue,endvalue);
		for(iY = startvalue; iY < endvalue; iY++)
		{
			
			Cy = CyMin + (iY * PixelHeight);
			if (fabs(Cy) < (PixelHeight / 2))
			{
				Cy = 0.0; /* Main antenna */
			}

			for(iX = 0; iX < iXmax; iX++)
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
			//for each iY 8000 times, total iX data(24000) will be sent to rank 0
			//MPI_Send(temp,iXmax*3 , MPI_UNSIGNED_CHAR, 0, 0, MPI_COMM_WORLD);
			

		}
		
		MPI_Send(temp,screen_per_procs * iXmax * 3 , MPI_UNSIGNED_CHAR, 0, 0, MPI_COMM_WORLD); 
		
		
		//printf("process %d successfully send.\n",rank);
	}
	// Get the clock current time again
	// Subtract end from start to get the CPU time used.
	
	if(rank ==0){
		end = MPI_Wtime();
		
		cpu_time_used = ((double)(end - start));

		fclose(fp);

		printf("Completed Computing Mandelbrot Set.\n");
		printf("File: %s successfully closed.\n", filename);
		printf("Mandelbrot computational process time: %lf\n", cpu_time_used);
		end = MPI_Wtime();
		cpu_time_used = ((double)(end - overall)) ;
		printf("Mandelbrot overall time: %lf\n", cpu_time_used);
        
	}
	
    MPI_Finalize();
	return 0;
}

