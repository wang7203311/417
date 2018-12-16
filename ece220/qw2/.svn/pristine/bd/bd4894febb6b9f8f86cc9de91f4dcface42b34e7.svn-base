#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "mp8.h"


/*
 * basicRecurse -- flood fill recursively from a point until reaching
 *                 black or the image border
 * INPUTS: width -- width of the input image
 *         height -- height of the input image
 *         inRed -- pointer to the input red channel (1-D array)
 *         inGreen -- pointer to the input green channel (1-D array)
 *         inBlue -- pointer to the input blue channel (1-D array)
 *         x -- current x position of the flood
 *         y -- current y position of the flood
 *         marking -- array used to mark seen positions (indexed
 *                    in the same way as the RGB input arrays)
 * OUTPUTS: marking -- marked with flooded pixels
 * RETURN VALUE: none
 * SIDE EFFECTS: none
 */
/*check the boundary condition first, then check the condition of pixel, if it is marked or
black, we retun. then mark the pixel and check next pixel in the following order:
up, right, down, left.*/
void
basicRecurse (int32_t width, int32_t height,
	      const uint8_t* inRed, const uint8_t* inGreen,
	      const uint8_t* inBlue,
	      int32_t x, int32_t y,
	      uint8_t* marking)
{
		// check the boundary condition, if it is beyond bound, return back
			if(x >= width || y >= height || x <0 || y< 0)
			{
				return;
			}
			int32_t index = x + y*width; //calculate the index value
			//check if the pixel is marked or black pixel, if yes we return
			if(marking[index] == 1 ||(inRed[index] == 0 && inGreen[index] == 0 && inBlue[index] == 0))
			 {
				 return;
			 }
			 	//the pixel is "safe" pixel
				marking[index] = 1; //mark that pixel
				basicRecurse(width, height, inRed, inGreen, inBlue, x , y-1, marking);	//go to recurse function, check the upside pixel
				basicRecurse(width, height, inRed, inGreen, inBlue, x+1 , y, marking);  //go to recurse function, check the rightside pixel
				basicRecurse(width, height, inRed, inGreen, inBlue, x , y+1, marking);  //go to recurse function, check the bottom pixel
				basicRecurse(width, height, inRed, inGreen, inBlue, x-1 , y, marking);	//go to recurse function, check the leftside pixel
}


/*
 * greyRecurse -- flood fill recursively from a point until reaching
 *                near-black pixels or the image border
 * INPUTS: width -- width of the input image
 *         height -- height of the input image
 *         inRed -- pointer to the input red channel (1-D array)
 *         inGreen -- pointer to the input green channel (1-D array)
 *         inBlue -- pointer to the input blue channel (1-D array)
 *         x -- current x position of the flood
 *         y -- current y position of the flood
 *         distSq -- maximum distance squared between black and boundary
 *                   pixel color
 *         marking -- array used to mark seen positions (indexed
 *                    in the same way as the RGB input arrays)
 * OUTPUTS: marking -- marked with flooded pixels
 * RETURN VALUE: none
 * SIDE EFFECTS: none
 */
 /*check the boundary condition first, then check the condition of pixel, if it is marked or
 near black(use colorsWithinDistSq function, if return 1 means it close to black), we retun.
then mark the pixel and check next pixel in the following order:
 up, right, down, left.*/
void
greyRecurse (int32_t width, int32_t height,
	     const uint8_t* inRed, const uint8_t* inGreen,
	     const uint8_t* inBlue,
	     int32_t x, int32_t y, uint32_t distSq,
	     uint8_t* marking)
{
  if(x >= width || y >= height || x <0 || y< 0)//check the boundary condition, if it is out of bound, return back
	{
	 return;
	}
	int32_t index = x + y *width; //calculate the index value
	if(marking[index] == 1 || colorsWithinDistSq(0,0,0,inRed[index],inGreen[index],inBlue[index], distSq)) //check if the pixel is marked or near black pixel
	{
		return; //if yes, return
	}
			marking[index] = 1; //mark the pixel
			greyRecurse(width, height, inRed, inGreen, inBlue, x , y-1,distSq, marking);//go to recurse function, check the upside pixel
		  greyRecurse(width, height, inRed, inGreen, inBlue, x+1 , y,distSq, marking);//go to recurse function, check the rightside pixel
			greyRecurse(width, height, inRed, inGreen, inBlue, x , y+1,distSq, marking);//go to recurse function, check the bottom pixel
			greyRecurse(width, height, inRed, inGreen, inBlue, x-1 , y,distSq, marking);//go to recurse function, check the leftside pixel
}
/*
 * limitedRecurse -- flood fill recursively from a point until reaching
 *                   pixels too different (in RGB cor) from the color at
 *                   the flood start point, too far away (> 40 pixels), orgo to recurse funtion,yond the image border
 * INPUTS: width -- width of the input image
 *         height -- height of the input image
 *         inRed -- pointer to the input red channel (1-D array)
 *         inGreen -- pointer to the input green channel (1-D array)
 *         inBlue -- pointer to the input blue channel (1-D array)
 *         origX -- starting x position of the flood
 *         origY -- starting y position of the flood
 *         x -- current x position of the flood
 *         y -- current y position of the flood
 *         distSq -- maximum distance squared between pixel at origin
 *                   and boundary pixel color
 *         marking -- array used to mark seen positions (indexed
 *                    in the same way as the RGB input arrays)
 * OUTPUTS: marking -- marked with flooded pixels
 * RETURN VALUE: none
 * SIDE EFFECTS: none
 */
 /*check the boundary condition first, then check the condition of pixel, if it is marked or
 farway to original color(use colorsWithinDistSq function, if return 1 means it close to original color), we retun.
 then mark the pixel and check next pixel in the following order:
 up, right, down, left.*/
void
limitedRecurse (int32_t width, int32_t height,
	        const uint8_t* inRed, const uint8_t* inGreen,
	        const uint8_t* inBlue,
	        int32_t origX, int32_t origY, int32_t x, int32_t y,
		uint32_t distSq, uint8_t* marking)
{
	int32_t distanceSq = (x-origX)*(x-origX) + (y-origY)*(y-origY);//check the distance between the pixel and origin
	if(distanceSq > 1600) //if that is too farway (>40 pixels), return back
	{
		return;
	}
	if(x<0  || x >=width || y <0 || y>=height) //check the boundary condition, if it is out of bound retun
	{
		return;
	}
	int32_t startindex = origX + origY*width; //calculate the index of origin
	int32_t index = x + y*width; //check the index of the pixel
	//check if the pixel is marked our the color is too different (in RGB color) from the color at the flood start point.
	if(marking[index] == 1 || !(colorsWithinDistSq(inRed[startindex], inGreen[startindex], inBlue[startindex], inRed[index], inGreen[index],inBlue[index], distSq)))
		 {
			 return; //if yes, retun;
		 }
			marking[index] = 1; //mark the pixel
	limitedRecurse(width, height, inRed, inGreen, inBlue, origX, origY, x, y-1, distSq, marking);//go to recurse funtion,check the upside pixel
	limitedRecurse(width, height, inRed, inGreen, inBlue, origX, origY, x+1, y, distSq, marking);//go to recurse funtion,check the rightside pixel
	limitedRecurse(width, height, inRed, inGreen, inBlue, origX, origY, x, y+1, distSq, marking);//go to recurse funtion,check the bottom pixel
	limitedRecurse(width, height, inRed, inGreen, inBlue, origX, origY, x-1, y, distSq, marking);//go to recurse funtion,check the leftside pixel
}
