/*									tab:8
 *
 * mp6.c - implementation file for ECE220 "Blocky" game
 *
 * "Copyright (c) 2017-2018 by Steven S. Lumetta."
 *
 * Permission to use, copy, modify, and distribute this software and its
 * documentation for any purpose, without fee, and without written agreement is
 * hereby granted, provided that the above copyright notice and the following
 * two paragraphs appear in all copies of this software.
 *
 * IN NO EVENT SHALL THE AUTHOR OR THE UNIVERSITY OF ILLINOIS BE LIABLE TO
 * ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL
 * DAMAGES ARISING OUT  OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION,
 * EVEN IF THE AUTHOR AND/OR THE UNIVERSITY OF ILLINOIS HAS BEEN ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * THE AUTHOR AND THE UNIVERSITY OF ILLINOIS SPECIFICALLY DISCLAIM ANY
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE SOFTWARE
 * PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND NEITHER THE AUTHOR NOR
 * THE UNIVERSITY OF ILLINOIS HAS ANY OBLIGATION TO PROVIDE MAINTENANCE,
 * SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS."
 *
 * Author:	    Steve Lumetta
 * Version:	    5
 * Creation Date:   7 November 2017
 * Filename:	    mp2.c
 * History:
 *	SL	1	7 November 2017
 *		First written.
 *      JXG     2	8 November 2017
 *		Added ncurses support.
 *	SL	3	30 November 2017
 *		Polished for MP distribution.
 *	SL	4	18 February 2018
 *		Edited slightly for ECE220H S18 distribution.
 *	SL	5	18 February 2018
 *		Stripped down from gold version.
 */


#include <stdint.h>
#include <stdio.h>

#include "mp6.h"


/*
 * The maximum number of blocks in one piece.  Do not change for
 * this assignment (you can do as you like with the code afterward).
 */
#define MAX_PIECE_SIZE 4

/*
 * Pieces are defined by an array of offsets from the center point.
 * Each piece consists of a set of adjacent blocks that together form
 * the piece.  The first index of the array is the piece type, the
 * second is the orientation (0-3), the third is block index within
 * the piece (0 to MAX_PIECE_SIZE - 1), and the fourth gives the
 * x (0) and y (1) offsets of the block relative to the center point.
 * Note that the first block is always the center point of the piece.
 *
 * Offsets may be replicated if a piece contains fewer than MAX_PIECE_SIZE
 * blocks.
 *
 * Clockwise rotation changes the orientation in the positive (mod 4)
 * direction, and counter-clockwise rotation changes the orientation in
 * the negative (mod 4) direction.
 */
static const int32_t piece_def[NUM_PIECE_TYPES][4][MAX_PIECE_SIZE][2] = {
    {   /* PIECE_TYPE_ELL */
	{{0, 0}, { 1,  0}, { 2,  0}, { 0,  1}},
	{{0, 0}, { 0,  1}, { 0,  2}, {-1,  0}},
	{{0, 0}, {-1,  0}, {-2,  0}, { 0, -1}},
	{{0, 0}, { 0, -1}, { 0, -2}, { 1,  0}}
    },
    {   /* PIECE_TYPE_REV_ELL */
	{{0, 0}, { 1,  0}, { 2,  0}, { 0, -1}},
	{{0, 0}, { 0,  1}, { 0,  2}, { 1,  0}},
	{{0, 0}, {-1,  0}, {-2,  0}, { 0,  1}},
	{{0, 0}, { 0, -1}, { 0, -2}, {-1,  0}}
    },
    {   /* PIECE_TYPE_LINE */
	{{0, 0}, {-1,  0}, { 1,  0}, { 2,  0}},
	{{0, 0}, { 0, -1}, { 0,  1}, { 0,  2}},
	{{0, 0}, { 1,  0}, {-1,  0}, {-2,  0}},
	{{0, 0}, { 0,  1}, { 0, -1}, { 0, -2}}
    },
    {   /* PIECE_TYPE_TEE */
	{{0, 0}, {-1,  0}, { 0, -1}, { 1,  0}},
	{{0, 0}, { 0, -1}, { 1,  0}, { 0,  1}},
	{{0, 0}, { 1,  0}, { 0,  1}, {-1,  0}},
	{{0, 0}, { 0,  1}, {-1,  0}, { 0, -1}}
    },
    {   /* PIECE_TYPE_ESS */
	{{0, 0}, { 0, -1}, { 1,  0}, { 1,  1}},
	{{0, 0}, { 1,  0}, { 0,  1}, {-1,  1}},
	{{0, 0}, { 0,  1}, {-1,  0}, {-1, -1}},
	{{0, 0}, {-1,  0}, { 0, -1}, { 1, -1}}
    },
    {   /* PIECE_TYPE_REV_ESS */
	{{0, 0}, { 0, -1}, {-1,  0}, {-1,  1}},
	{{0, 0}, { 1,  0}, { 0, -1}, {-1, -1}},
	{{0, 0}, { 0,  1}, { 1,  0}, { 1, -1}},
	{{0, 0}, {-1,  0}, { 0,  1}, { 1,  1}}
    }
};
/*
 * empty_board -- fills a board b with empty spaces (SPACE_EMPTY)
 * INPUTS: b -- the board
 * OUTPUTS: b -- the board, filled with empty spaces
 * RETURN VALUE: none
 * SIDE EFFECTS: none
 */
 /*work though the array row by row, the end point of one row is BOARD_WIDTH -1
 and the index of the last row is BOARD_HEIGHT-1 */
int32_t
empty_board (space_type_t b[BOARD_HEIGHT][BOARD_WIDTH])
{
  int32_t i; //the index of the element is one row
  int32_t j; // the index of the row
  {
      for(j = 0; j < BOARD_HEIGHT; j++) //the loop will end until it reach the index of BOARD_HEIGHT
       {
          for(i = 0; i < BOARD_WIDTH; i++ ) //the loop will end until it reach the indext of BOARD_WIDTH
            {
               b[j][i] = SPACE_EMPTY;   //the place of a specific point
           }
       }
    return 1;   //return 1 if it success
  }
   return 0;    //return 0 for fail
}


/*
 * mark_piece -- forcibly writes a piece into a board, ignoring the
 *               board's current contents; you will need to understand
 *               the piece definition array (piece_def) in order to
 *               implement this function
 * INPUTS: b -- the board
 *         p -- the type of piece
 *         orient -- the orientation of the piece
 *         x -- horizontal coordinate of the piece's center point
 *         y -- vertical coordinate of the piece's center point
 *         v -- type of space to write (in the shape of the piece)
 * OUTPUTS: b -- the board, with the piece filled in with value v
 * RETURN VALUE: none
 * SIDE EFFECTS: none
 */
void
/*find the point by the array it given and fill with the some type of space */
mark_piece (space_type_t b[BOARD_HEIGHT][BOARD_WIDTH],
            piece_type_t p, int32_t orient, int32_t x, int32_t y,
	    space_type_t v)
{
  int32_t i;    // it is the element of one piece
  int32_t j;    // it is x offset if it is 0 and y offset if it is 1
  int32_t x_coord;  //the x coordinate of the element of one piece
  int32_t y_coord;  // the y coordinate of the element of one piece
  for (i = 0; i < MAX_PIECE_SIZE; i++)  //the loop will end until it reach the MAX_PIECE_SIZE
    {
      for (j = 0; j < 2; j++)   // the loop will end until it is 2
        {
            if(j == 0)    // check if it is x offset or y offset
             {
              x_coord = piece_def[p][orient][i][j] + x;   //find the x coordinate
             }
           else
             {
              y_coord =piece_def[p][orient][i][j]+y;    // find the y coordinate
             }
        }
     b[y_coord][x_coord] = v;   //fill some type of space
    }
}


/*
 * test_piece_fit -- checks whether a piece fits into a board; you will
 *		     need to understand the piece definition array
 *		     (piece_def) in order to implement this function
 * INPUTS: b -- the board
 *         p -- the type of piece
 *         orient -- the orientation of the piece
 *         x -- horizontal coordinate of the piece's center point
 *         y -- vertical coordinate of the piece's center point
 * OUTPUTS: none
 * RETURN VALUE: if the piece does not fit within the board, returns
 *		 FIT_OUT_OF_BOARD; otherwise, if the piece would overwrite
 *		 non-empty board spaces, returns FIT_NO_ROOM_THERE;
 *		 otherwise, returns FIT_SUCCESS
 * SIDE EFFECTS: none
 */
fit_result_t
/* First find if this piece beyond the bounds, check it element
by element. If not check if there is element already occupy here. if pass
there two testm we said that it is unoccupied Place*/
test_piece_fit (space_type_t b[BOARD_HEIGHT][BOARD_WIDTH],
                piece_type_t p, int32_t orient, int32_t x, int32_t y)
{
    int32_t i;    //one element of one piece
    int32_t j;    // x or y offset, 0 for x and 1 for y
    int32_t test_x;   // the x coordinate of one element
    int32_t test_y;   // the y coordinate of one element
    for (i = 0; i < MAX_PIECE_SIZE; i++)  // the loop will end until it reach the MAX_PIECE_SIZE
      {
        for (j = 0; j < 2; j++)   //the loop will end until it reach 2
         {
              if(j == 0)      // check if it is x offset or y offset
               {
                test_x = piece_def[p][orient][i][j] + x;    //find the x coordinate of one element
               }
             else
               {
                test_y = piece_def[p][orient][i][j] + y;  // find the y coordinate of one element
               }
         }
//check if it is beyond the bound
      if(test_x >= BOARD_WIDTH || test_x <0 || test_y >= BOARD_HEIGHT || test_y< 0)
        {
              return FIT_OUT_OF_BOARD;
        }
      else if (b[test_y][test_x] != SPACE_EMPTY) // check if it is occupied point
        {
              return FIT_NO_ROOM_THERE;
        }
      }
    return FIT_SUCCESS; //return success
}


/*
 * print_board -- prints a board to the screen using period ('.') to
 *		  represent empty spaces, percent ('%') to represent
 *		  old blocks, and asterisk ('*') to represent the current
 *		  piece (SPACE_BLOCK); see specification for example
 * 		  of board appearance
 * INPUTS: b -- the board
 * OUTPUTS: none
 * RETURN VALUE: none
 * SIDE EFFECTS: prints to the monitor
 */
/*print this board row by row. different space type corresponding to
different sign*/
void
print_board (space_type_t b[BOARD_HEIGHT][BOARD_WIDTH])
{
  int32_t i;  // the index of the row
  int32_t j;  // the index of one element in one row
for(j = 0; j < BOARD_HEIGHT; j++) //the loop will end until it reach BOARD_HEIGHT
 {
   for(i = 0; i < BOARD_WIDTH; i++ )  //the loop will end until it reach BOARD_WIDTH
   {
     if (b[j][i] == SPACE_EMPTY)  // check if it is SPACE_EMPTY
     {
       printf(".");
     }
     else if (b[j][i] == SPACE_BLOCK) //check if it is SPACE_BLOCK
      {
        printf("*");
      }
      else
      {
        printf("%%"); // if it is not SPACE_EMPTY or SPACE_BLOCK
      }
   }
   printf("\n"); //print new line
 }
}

/*
 * try_to_move_down -- tries to move the current piece down one space in
 *                     the board; assumes that the piece is in the board
 *		       and must thus be removed before it can be put into
 *                     its new position (or back into its old position
 *                     on failure)
 * INPUTS: b -- the board
 *         p -- the type of piece
 *         orient -- the current orientation of the piece
 *         x -- current horizontal coordinate of the piece's center point
 *         y -- current vertical coordinate of the piece's center point
 * OUTPUTS: b -- the board, with the piece moved down (on success), or
 *               unchanged on failure
 * RETURN VALUE: 1 on success, 0 on failure
 * SIDE EFFECTS: none
 */
int32_t
/*because we only need to make it move down in one row, we just need
to make the center point move down one row that is increase the y coordinate
by 1*/
try_to_move_down (space_type_t b[BOARD_HEIGHT][BOARD_WIDTH],
                  piece_type_t p, int32_t orient, int32_t x, int32_t y)
{
          remove_piece(b,p, orient, x, y); //call the remove piece function
        if(FIT_OUT_OF_BOARD == test_piece_fit (b,p,orient,x, y+1) //check if the new position beyond the board
         || FIT_NO_ROOM_THERE ==test_piece_fit (b,p,orient,x,y+1))  // check if the new position already occupied
        {
          add_piece(b,p,orient,x,y);  // if yes, add the piece back
          return 0; //return fail
        }
        else
        {
          add_piece(b,p,orient,x,y+1); // move the the new position
          return 1; //return success
        }
}


/*
 * try_to_move_left -- tries to move the current piece one space left in
 *                     the board; assumes that the piece is in the board
 *		       and must thus be removed before it can be put into
 *                     its new position (or back into its old position
 *                     on failure)
 * INPUTS: b -- the board
 *         p -- the type of piece
 *         orient -- the current orientation of the piece
 *         x -- current horizontal coordinate of the piece's center point
 *         y -- current vertical coordinate of the piece's center point
 * OUTPUTS: b -- the board, with the piece moved left (on success), or
 *               unchanged on failure
 * RETURN VALUE: 1 on success, 0 on failure
 * SIDE EFFECTS: none
 */
 /*because we only need to make it move left in one row, we just need
 to make the center point move left one colomn that is increase the x coordinate
 by -1*/
int32_t
try_to_move_left (space_type_t b[BOARD_HEIGHT][BOARD_WIDTH],
                  piece_type_t p, int32_t orient, int32_t x, int32_t y)
{
        remove_piece(b,p, orient, x, y); //remove the original piece
/*check if the new position beyond the board and  check if the new position already occupied*/
        if(FIT_OUT_OF_BOARD == test_piece_fit (b,p,orient,(x-1), y)
        || FIT_NO_ROOM_THERE ==test_piece_fit (b,p,orient,(x-1),y))
      {
        add_piece(b,p,orient,x,y); // if yes return back
          return 0;   //return fail
      }
        else
      {
        add_piece(b,p,orient,x-1,y); //if no fo to the new position
       return 1; //return success
      }
}


/*
 * try_to_move_right -- tries to move the current piece one space right in
 *                     the board; assumes that the piece is in the board
 *		       and must thus be removed before it can be put into
 *                     its new position (or back into its old position
 *                     on failure)
 * INPUTS: b -- the board
 *         p -- the type of piece
 *         orient -- the current orientation of the piece
 *         x -- current horizontal coordinate of the piece's center point
 *         y -- current vertical coordinate of the piece's center point
 * OUTPUTS: b -- the board, with the piece moved right (on success), or
 *               unchanged on failure
 * RETURN VALUE: 1 on success, 0 on failure
 * SIDE EFFECTS: none
 */
 /*because we only need to make it move right in one row, we just need
 to make the center point move right one colomn that is increase the x coordinate
 by 1*/
 int32_t
try_to_move_right (space_type_t b[BOARD_HEIGHT][BOARD_WIDTH],
                   piece_type_t p, int32_t orient, int32_t x, int32_t y)
{
        remove_piece(b,p, orient, x, y); //remove the original piece
/*check if the new position beyond the board and  check if the new position already occupied*/
        if(FIT_OUT_OF_BOARD == test_piece_fit (b,p,orient,x+1, y)
            || FIT_NO_ROOM_THERE ==test_piece_fit (b,p,orient,x+1,y))
           {
              add_piece(b,p,orient,x,y); //if yes go to the original place
              return 0; //return fail
           }
        else
           {
              add_piece(b,p,orient,x+1,y); //go to the new place
              return 1; //return fail
           }
}
/*
 * try_to_rotate_clockwise --
 *	tries to rotate the current piece clockwise in the board; assumes
 *	that the piece is in the board and must thus be removed before it
 *	can be put into its new position (or back into its old position on
 *	failure)
 * INPUTS: b -- the board
 *         p -- the type of piece
 *         orient -- the current orientation of the piece
 *         x -- current horizontal coordinate of the piece's center point
 *         y -- current vertical coordinate of the piece's center point
 * OUTPUTS: b -- the board, with the piece rotated clockwise (on success),
 *		 or unchanged on failure
 * RETURN VALUE: 1 on success, 0 on failure
 * SIDE EFFECTS: none
 */
 /*because we only need to make it rotate clockwise, we just need
 to make the orient parameter increase by 1*/
int32_t
try_to_rotate_clockwise (space_type_t b[BOARD_HEIGHT][BOARD_WIDTH],
                         piece_type_t p, int32_t orient, int32_t x, int32_t y)
{
            remove_piece(b,p, orient, x, y); //remove the piece
/*check if the new position beyond the board and  check if the new position already occupied
because the orient cannot beyond 3 we need to mod(4)*/
        if(FIT_OUT_OF_BOARD == test_piece_fit (b,p,(orient+1)%4,x, y)
                  || FIT_NO_ROOM_THERE ==test_piece_fit (b,p,(orient+1)%4,x,y))
            {
                add_piece(b,p,orient,x,y); //if yes return to original place
                return 0;   //return failure
            }
        else
            {
                add_piece(b,p,(orient+1)%4,x,y); //go to the new place
                return 1; //return success
            }
}


/*
 * try_to_rotate_cc --
 *	tries to rotate the current piece counter-clockwise in the board;
 *	assumes that the piece is in the board and must thus be removed
 *	before it can be put into its new position (or back into its old
 *	position on failure)
 * INPUTS: b -- the board
 *         p -- the type of piece
 *         orient -- the current orientation of the piece
 *         x -- current horizontal coordinate of the piece's center point
 *         y -- current vertical coordinate of the piece's center point
 * OUTPUTS: b -- the board, with the piece rotated counter-clockwise (on
 *		 success), or unchanged on failure
 * RETURN VALUE: 1 on success, 0 on failure
 * SIDE EFFECTS: none
 */
 /*because we only need to make it rotate counter-clockwise, we just need
 to make the orient parameter increase by 3*/
int32_t
try_to_rotate_cc (space_type_t b[BOARD_HEIGHT][BOARD_WIDTH],
                  piece_type_t p, int32_t orient, int32_t x, int32_t y)
{
  remove_piece(b,p, orient, x, y); //remove the piece
  /*check if the new position beyond the board and  check if the new position already occupied
  because the orient cannot beyond 3 we need to mod(4)*/
  if(FIT_OUT_OF_BOARD == test_piece_fit (b,p,(orient+3)%4,x, y)
        || FIT_NO_ROOM_THERE ==test_piece_fit (b,p,(orient+3)%4,x,y))
  {
      add_piece(b,p,orient,x,y); // return to old position
      return 0; //return fail
  }
  else
  {
      add_piece(b,p,(orient+3)%4,x,y); //return to new position
      return 1; //return success
  }
}


/*
 * remove_row -- removes a single row from a board, moving rows above
 *		 it downward and adding a new empty row at the top of
 *		 the board; this function should be called by your
 *		 remove_full_rows function
 * INPUTS: b -- the board
 *	   row -- which row to remove
 * OUTPUTS: b -- the board, with the specified row removed
 * RETURN VALUE: none
 * SIDE EFFECTS: none
 */
/*emoves a single row from a board, moving rows above
*		 it downward and adding a new empty row at the top of
*		 the board */
void
remove_row (space_type_t b[BOARD_HEIGHT][BOARD_WIDTH], int row)
{
   int32_t k; //the index of row
   int32_t l; // the index of the element in one row
   for(k = row; k > 0; k--) //the loop will end until it reach 0
      {
        for(l = 0; l< BOARD_WIDTH; l++) // the loop will end until it reach the BOARD_WIDTH
          {
              b[k][l] = b[k-1][l];  //moving the rows above it downward
          }
      }
   for(l = 0; l < BOARD_WIDTH; l++) //add a new empty row at top
      {
        b[0][l] = SPACE_EMPTY;
      }
}


/*
 * remove_full_rows -- removes all rows filled with SPACE_FULL from a
 * 		       board, moving rows above them downward and adding
 *		       new empty rows at the top of the board
 * INPUTS: b -- the board
 * OUTPUTS: b -- the board, with full rows removed
 * RETURN VALUE: none
 * SIDE EFFECTS: none
 */
/*check the board row by row, if there is a element which is not SPACE_FULL, we go
to the next row. if all the the element in one row is SPACE_FULL, we call remove_row*/
void
remove_full_rows (space_type_t b[BOARD_HEIGHT][BOARD_WIDTH])
{
   int32_t i; //the index of the row
   int32_t j; //the index of the element in one row
   for(i = 0; i < BOARD_HEIGHT; i++) //the loop will end until it reach the BOARD_HEIGHT
   {
     for(j = 0; j < BOARD_WIDTH; j++) // the loop will end until it reach the BOARD_WIDTH
      {
         if(b[i][j] != SPACE_FULL) //check if it is SPACE_FULL
         {
           break;   //if not SPACE_FULL, break and go to next row
         }
         if(j == BOARD_WIDTH -1) //check if we reach the end of the row
         {
           remove_row(b, i); // call remove_row
         }
      }
   }
}
