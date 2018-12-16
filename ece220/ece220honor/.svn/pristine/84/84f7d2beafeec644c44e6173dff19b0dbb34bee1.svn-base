/*
 * ECE220 Spring 2018
 *
 * Program name: prmain.c, a driver for a buggy version of the
 *               recursive backwards string printer
 *
 * Description: This program calls reverse_print on all command-line
 *              arguments, printing each in reverse along with its
 *              length.
 */


#include <stdint.h>       /* Include C's standard integer header file.      */
#include <stdio.h>        /* Include C's standard I/O header file.          */

// the function in pr_buggy.c
int32_t print_reverse (const char* s);

int 
main (int argc, const char* const argv[])
{
    int32_t i;	// iteration variable over command-line arguments

    if (2 > argc) {
        fprintf (stderr, "syntax: %s <string1> <string2> ...\n", argv[0]);
	return 2;
    }

    for (i = 1; argc > i; i++) {
	// Print reversed string and length
	printf ("\"%s\" reversed is \"", argv[i]);
	printf ("\" (length %d)\n", print_reverse (argv[i]));
    }

    return 0;
}


