// introduction
/*
We first construct the base case that is there is no blank at end and the blank between the
two contiguous black region is 1. Then the remaining blanks are placed inflont of the first
black region.
After that, we manipulate the blank until on blank infront of the fist region and all remaining
blanks are place after r4. Everytime we manipulate the sequence, we '&' with the previous sequence
and store it as the result sequence. After all, we use the maskvector to print the result sequence
1 is for 'X' and 0 for '.'
*/
#include <stdio.h>
#include "mp4.h"
/* the function used to ptint the result */
void printVector(uint64_t vector, int32_t width) {
    uint64_t mask = (uint64_t)0x1 << (width-1);
    // construct the mask vector
    int32_t i;
    for ( i = 0; i < width; i++)
    //loop body
    {
        if (vector << i & mask) printf("X");
        else printf(".");
    }
    printf("\n");
}
int32_t print_row(int32_t r1, int32_t r2, int32_t r3, int32_t r4, int32_t width) {
    // Construct 4 vectors base on the value of r1, r2, r3, r4
    // define the variable
    uint64_t r1Vector = 0;
    uint64_t r2Vector = 0;
    uint64_t r3Vector = 0;
    uint64_t r4Vector = 0;
    int32_t j;
    int32_t k;
    int32_t l;
    int32_t m;
    for ( j = 0; j < r1; j++)
    {r1Vector = r1Vector << 1 | 1;} // use left shift to construct r1Vector
    for ( k = 0; k < r2; k++)
    {r2Vector = r2Vector << 1 | 1;} // use left shift to construct r2Vector
    for ( l = 0; l < r3; l++)
    {r3Vector = r3Vector << 1 | 1;} // use left shift to construct r3Vector
    for ( m = 0; m < r4; m++)
    {r4Vector = r4Vector << 1 | 1;} // use left shift to construct r4Vector

    // Construct 5 gaps between two contiguous black region
    // define the varaiable
    int32_t g2 = 0;
    int32_t g3 = 0;
    int32_t g4 = 0;
    int32_t g5 = 0;
    //deal with the 0-length region
    if (r2 != 0)
    { g2 = 1;}
    if (r3 != 0)
    {g3 = 1;}
    if (r4 != 0)
    {g4 = 1;}
    int32_t g1 = width - r1 - g2 - r2 - g3 - r3 - g4 - r4;
    int32_t g1default = g1;


    // Check argument validity
    if (g1default < 0) {
        return 0; // Impossible
    }
    // Construct base case, use left shift to build the base case.
    uint64_t resultVector = 0; // Since width is 50, smaller than 64
    resultVector = resultVector << g1;  //left shift g1 times
    resultVector = resultVector << r1 | r1Vector; // left shift r1 times and OR with r1Vector
    resultVector = resultVector << g2; //left shift g2 times
    resultVector = resultVector << r2 | r2Vector; // left shift r2 times and OR with r2Vector
    resultVector = resultVector << g3;// left shift g3 times
    resultVector = resultVector << r3 | r3Vector; // left shift r3 times and OR with r3Vector
    resultVector = resultVector << g4;// left shift g4 times
    resultVector = resultVector << r4 | r4Vector;// left shift r4 times and OR with r4Vector
    resultVector = resultVector << g5;// left shift g5 times
    printf("base case\n");
      printVector(resultVector, width);
    uint64_t tempVector = resultVector;
    while (g5 != g1default) { // Check if we moved all zeros to the end
        resultVector = tempVector << 1;
        tempVector = tempVector & resultVector;
        g5++;
        printVector(tempVector, width);
    }
    printf("final result\n");
    printVector(tempVector, width); //call the printVector function
    return 1;
}
