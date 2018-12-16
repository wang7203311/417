//									tab:8
//
// mp12.cpp - source file for Spring 2018 MP12 student code
//
// "Copyright (c) 2018 by Steven S. Lumetta."
//
// Permission to use, copy, modify, and distribute this software and its
// documentation for any purpose, without fee, and without written agreement is
// hereby granted, provided that the above copyright notice and the following
// two paragraphs appear in all copies of this software.
//
// IN NO EVENT SHALL THE AUTHOR OR THE UNIVERSITY OF ILLINOIS BE LIABLE TO
// ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL
// DAMAGES ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION,
// EVEN IF THE AUTHOR AND/OR THE UNIVERSITY OF ILLINOIS HAS BEEN ADVISED
// OF THE POSSIBILITY OF SUCH DAMAGE.
//
// THE AUTHOR AND THE UNIVERSITY OF ILLINOIS SPECIFICALLY DISCLAIM ANY
// WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
// MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE SOFTWARE
// PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND NEITHER THE AUTHOR NOR
// THE UNIVERSITY OF ILLINOIS HAS ANY OBLIGATION TO PROVIDE MAINTENANCE,
// SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS."
//
// Author:	    Steve Lumetta
// Version:	    1.00
// Creation Date:   20 April 2018
// Filename:	    mp12.cpp
// History:
//	SL	1.00	20 April 2018
//		First written.
//

#include <iostream>
#include <list>

#include <math.h>
#include <stdio.h>

#include "WALYmain.h"

#include "TurtleScreen.h"

#include "mp5.h"
#include "mp12.h"

using namespace std;
using namespace WALY;

// THESE ARE GLOBAL VARIABLES IN THE INTEREST OF TESTING.  THEY SHOULD
// BE FILE-SCOPE OR LOCAL TO frameUpdate.
FILE*           input = NULL;		// input stream
list<segment_t> lines;			// list of lines drawn
command_t       cmd = {CMD_NONE};	// current command
int32_t	        moveColor = 0xFFFFFF;	// current movement drawing color

int32_t
openInputStream (const char* fname)
{
    if(NULL == (input = fopen(fname,"r"))) //check if we open successfully
    {
      return 0; //if we return 0 means we fail
    }
    else
    {
      return 1; //retur 1 for open successfully
    }
}

void
closeInputStream (void)
{
    if(input != NULL)
    {
      fclose(input);    //close the file
    }
}
void
showLines (void)
{
    // you can use 'call showLines ()' in GDB to look at the
    // list of segments.  Don't forget to call makeVisibleChange
    // when you change this list, since the background won't be
    // redrawn unless you call that function (so changes will not
    // show up.
    for (list<segment_t>::iterator it = lines.begin ();
	 lines.end () != it; it++) {
Screen::debug () << it->color << " " << it->x1 << "," << it->y1 << "  " << it->x2 << "," << it->y2 << endl;
    }
}

void
drawEverything (void)
{
  if(lines.empty ()) //check if the list is enpty
  {
    return;
  }
  for(list<segment_t>::iterator it = lines.begin();lines.end() != it ; it++) //use the iterator to traverse the list
  {
    set_color(it->color);
    draw_line(it->x1, it->y1, it->x2, it->y2);//draw line in the list
  }
}

void
readNewCommand (TurtleScreen* ts)
{
  int32_t size = 200;//set the size of the buffer
  char cmd_ar[8]; //set a buffer to store the command string
  char c; //used to check grabage
  char com[size+1];//command lines of 200 characters should be supported
  int32_t i;//use for parameter
  int32_t j;//used for parameter
  int32_t ang;//get the angle
  if (fgets(com, size, input) == NULL) //check if we reach the end of the file
    {
      //reach the end
      cmd.type = CMD_NONE; //change the type to none and return
      return;
    }
  else
  {
      sscanf(com,"%s", cmd_ar); //check the command strng
      if(!strcasecmp(cmd_ar,"color")) //if it is color command
      {
        if(sscanf(com, "%s %x %1s", cmd_ar, &i, &c) == 2) //check it is not ot lack of parameter grabage
        {
          moveColor = i;  //store the color parameter
        cmd.type = CMD_NONE; //change the type to none
        return; //return
        }
      }
      else if(!strcasecmp(cmd_ar,"move")) //if the command is move
      {
        if(sscanf(com, "%s%d%d%1s",cmd_ar, &i, &j, &c) == 3) //check it is not grabage or lack of parameter
        {
          cmd.endX = i; //dist
          cmd.cmdFrames = j; //frame
          cmd.framesLeft = j;//frame

          cmd.startX = ts->getX();//get the start point
          cmd.startY = ts->getY();//get the start point
          ang = (ts->getDirection() + 9);//get the direction
          cmd.endX = cmd.startX + round(i*cos(((M_PI*ang) / 18)));//use geometry to get end x
          cmd.endY = cmd.startY + -1*round(i*sin(((M_PI*ang) / 18)));//use geometry to get end y
          segment_t new_ls; //create a new line
          new_ls.color = moveColor;//set color and end and start point
          new_ls.x1 = cmd.startX;
          new_ls.y1 = cmd.startY;
          new_ls.x2 = cmd.endX;
          new_ls.y2 = cmd.endY;
          lines.push_back(new_ls);//push that to list

          cmd.type = CMD_MOVE;//change the type
          return;//return
        }
      }
      else if(!strcasecmp(cmd_ar, "restart")) //check if it is restart
      {
        if(sscanf(com, "%s%1s",cmd_ar, &c) == 1) //chek if it is grabage or lack of parameter
        rewind(input);//rewind the stream
        cmd.type = CMD_NONE; //change the type
        return;
      }
      else if(!strcasecmp(cmd_ar,"turn")) //check if it is the turn
      {
        if(sscanf(com, "%s%d%1s", cmd_ar, &i, &c) == 2) //check if it is grabage or lack of parameter
          {
            cmd.type = CMD_TURN; //change the type
            if(i<0)//check the direction
           {
            cmd.dir = -1;
            cmd.cmdFrames = -1*i; //set frame
            cmd.framesLeft = -1*i;
           }
           else
          {
            cmd.dir = 1;//set direction
            cmd.cmdFrames = i;//set frame
            cmd.framesLeft = i;
          }
        return;
        }
    }
      else if(!strcasecmp(cmd_ar,"wait")) //check if it is wait
      {
        {
        if(sscanf(com, "%s%d%1s",cmd_ar, &i, &c) == 2)//check it is not grabage and lack of parameter
          {
            cmd.cmdFrames = i; //set the frame
            cmd.framesLeft = i;
            cmd.type = CMD_WAIT;//change the type
            return;
          }
        }
      }
        fprintf(stderr, "Unrecognize command: %s", com);; //print out thr error message
  }

}

void
frameUpdate (TurtleScreen* ts)
{
  int32_t x_end;//the end point
  int32_t y_end;//the end point
  double y_buf = 0;//used to store how many pixel should move per pixel in y direction
  double x_buf = 0;//used to store how many pixel should move per pixel in x direction
  if(cmd.framesLeft == 0) //check if we have unfinished frame
  {
    cmd.type = CMD_NONE; //change the type
  }
  if(cmd.type == CMD_NONE) //if the command is none read new command
  {
    readNewCommand(ts);
  }
  else if(cmd.type == CMD_TURN) //turn
    {
      if(cmd.dir < 0) // turn right
      {
          ts->turnRight(); //call turn right function
          --(cmd.framesLeft); //decreament thr frame left
          ts->makeVisibleChange(); //make makeVisibleChange
      }
      else
      {
          ts->turnLeft(); //call turn left function
          --(cmd.framesLeft); //decreament the frame left
          ts->makeVisibleChange();//makeVisibleChange
      }
    }
   else if(cmd.type == CMD_MOVE)
   {
     --(cmd.framesLeft);//decreament the framesLeft
     x_buf = (cmd.cmdFrames - cmd.framesLeft)*(cmd.endX - cmd.startX)/(cmd.cmdFrames);//find the difference between start x and end for that frame
     y_buf = (cmd.cmdFrames - cmd.framesLeft)*(cmd.endY - cmd.startY)/(cmd.cmdFrames);//find the different between start y and end for that frame

     x_end = cmd.startX + x_buf;//find the end x
     y_end = cmd.startY + y_buf;//find the end y
     ts->setX(x_end);//set the new x for turtle
     ts->setY(y_end);//set the new y for turtle

    ts->makeVisibleChange();//makeVisibleChange
   }
   else if(cmd.type == CMD_WAIT)
   {
     --(cmd.framesLeft); //decreament the framesLeft
     ts->makeVisibleChange();//makeVisibleChange
   }
}
