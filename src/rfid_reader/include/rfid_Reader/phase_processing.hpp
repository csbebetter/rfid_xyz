#include <stdio.h>
#include <math.h>

double unwrappingPhase(double phasenow, double phaselast)
{   
    //Calculate the phase difference before and after
    double diff;
    if(phaselast>=0)
	{diff = phasenow - (phaselast-int(phaselast))-int(phaselast)%360;}
    if(phaselast<0)
    {diff = phasenow - (phaselast-int(phaselast))-(360+int(phaselast)%360);}
    //Other constants and variable definitions
	double pi = 180.0;
	double deviation = 90.0;
	double phasetemple = phaselast+diff;

	if(diff >= pi-deviation && diff <= pi+deviation){
		return (phasetemple-pi);
	}
	if(diff >= -pi-deviation && diff <= -pi+deviation){
		return (phasetemple+pi);
	}
    
	if(diff >= 2*pi-deviation && diff <= 2*pi+deviation){
		return (phasetemple-2*pi);
	}
	if(diff >= -2*pi-deviation && diff <= -2*pi+deviation){
		return (phasetemple+2*pi);
	}
    
	return phasetemple;
}

double caculate_initial_phase(double antenna[3],double tag[3]){
	double pi =3.141592768;
	return (4*pi/0.3125)*sqrt((antenna[0]-tag[0])*(antenna[0]-tag[0])+
							  (antenna[1]-tag[1])*(antenna[1]-tag[1])+
							  (antenna[2]-tag[2])*(antenna[2]-tag[2]));

}
