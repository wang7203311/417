/*									tab:8
 *
 * mp11.c - skeleton code generation for ECE190 compiler MP (F08 MP5)
 *
 * "Copyright (c) 2008-2018 by Steven S. Lumetta."
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
 * Version:	    3
 * Creation Date:   Wed Oct 15 10:16:14 2008
 * Filename:	    mp11.c
 * History:
 *	SL	3	Tue Apr 03 23:23:23 2018
 *		Changed MP5 to MP11 and 190 to 220 for ECE220.
 *	SL	2	Tue Oct 21 14:28:10 2008
 *		Extracted from gold version.
 *	SL	1	Wed Oct 15 10:16:14 2008
 *		First written.
 */


#include <stdio.h>

#include "ece220_label.h"
#include "ece220_parse.h"
#include "ece220_symtab.h"


/*
 * PARAMETERS AND CONSTANTS
 */

typedef enum {
    BR_NEVER, BR_P, BR_Z, BR_ZP, BR_N, BR_NP, BR_NZ, BR_ALWAYS, NUM_BR
} br_type_t;



/*
 * HELPER FUNCTION PROTOTYPES--see function headers for further information
 */

static void gen_long_branch (br_type_t type, ece220_label_t* label);

static void gen_statement (ast220_t* ast);
static void gen_for_statement (ast220_t* ast);
static void gen_if_statement (ast220_t* ast);
static void gen_return_statement (ast220_t* ast);
static void gen_pop_stack (ast220_t* ast);
static void gen_debug_marker (ast220_t* ast);

static void gen_expression (ast220_t* ast);
static void gen_push_int (ast220_t* ast);
static void gen_push_str (ast220_t* ast);
static void gen_push_variable (ast220_t* ast);
static void gen_func_call (ast220_t* ast);
static void gen_get_address (ast220_t* ast);
static void gen_op_assign (ast220_t* ast);
static void gen_op_pre_incr (ast220_t* ast);
static void gen_op_pre_decr (ast220_t* ast);
static void gen_op_post_incr (ast220_t* ast);
static void gen_op_post_decr (ast220_t* ast);
static void gen_op_add (ast220_t* ast);
static void gen_op_sub (ast220_t* ast);
static void gen_op_mult (ast220_t* ast);
static void gen_op_div (ast220_t* ast);
static void gen_op_mod (ast220_t* ast);
static void gen_op_negate (ast220_t* ast);
static void gen_op_log_not (ast220_t* ast);
static void gen_op_log_or (ast220_t* ast);
static void gen_op_log_and (ast220_t* ast);
static void gen_comparison (ast220_t* ast, const char* false_cond);
static void gen_op_cmp_ne (ast220_t* ast);
static void gen_op_cmp_less (ast220_t* ast);
static void gen_op_cmp_le (ast220_t* ast);
static void gen_op_cmp_eq (ast220_t* ast);
static void gen_op_cmp_ge (ast220_t* ast);
static void gen_op_cmp_greater (ast220_t* ast);


/*
 * FILE SCOPE VARIABLES
 *
 * N.B.  You will need to have a file scope variable to implement one
 * of the statements.  Define it here.
 *
 * static int foo;  <-- a file scope variable ("static" means only this file)
 *
 */



/*
 * INTERFACE FUNCTIONS -- called from other files; the one function listed
 * here is the equivalent of "main" for students working on this MP
 */

/*
 * MP11_generate_code
 *   DESCRIPTION: perform LC-3 code generation (print to stdout)
 *   INPUTS: prog -- the main subroutine of the program (a list of
 *                   statements)
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*travelsal all the statement and create a label for tear down code*/
static ece220_label_t* branch;/*create a label connect to tear down code*/
void
MP11_generate_code (ast220_t* prog)
{
  ast220_t** search;  /*define a double pointer for traversal the linkedlist*/
    branch = label_create();
    for(search = &prog; *search != NULL; search = &((*search)-> next))
    {
      gen_statement(*search);/*check the statement*/
    }
    printf("%s\n", label_value(branch)); /*label to tear down code*/
}

/*
 * HELPER FUNCTIONS (used only within this file)
 */

/*
 * gen_long_branch
 *   DESCRIPTION: generate LC-3 assembly code for a branch without offset
 *                limitations
 *   INPUTS: type -- the type of branch to be performed
 *           label -- the branch target label
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
static void
gen_long_branch (br_type_t type, ece220_label_t* label)
{
    static const char* const br_names[NUM_BR] = {
        "; ", "BRp", "BRz", "BRzp", "BRn", "BRnp", "BRnz", "BRnzp"
    };
    br_type_t neg_type;
    ece220_label_t* target_label;
    ece220_label_t* false_label;

    neg_type = (type ^ 7);
    target_label = label_create ();
    false_label = label_create ();
    printf ("\t%s %s\n", br_names[neg_type], label_value (false_label));
    printf ("\tLD R3,%s\n\tJMP R3\n", label_value (target_label));
    printf ("%s\n", label_value (target_label));
    printf ("\t.FILL %s\n", label_value (label));
    printf ("%s\n", label_value (false_label));
}

/*
 * gen_statement
 *   DESCRIPTION: generate LC-3 assembly code for an arbitrary statement
 *   INPUTS: ast -- the AST node corresponding to the statement
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
static void
gen_statement (ast220_t* ast)
{
    switch (ast->type) {
        case AST220_FOR_STMT:     gen_for_statement (ast);    break;
        case AST220_IF_STMT:      gen_if_statement (ast);     break;
        case AST220_RETURN_STMT:  gen_return_statement (ast); break;
        case AST220_POP_STACK:    gen_pop_stack (ast);        break;
        case AST220_DEBUG_MARKER: gen_debug_marker (ast);     break;
	default: fputs ("BAD STATEMENT TYPE\n", stderr);      break;
    }
}

/*
 * gen_for_statement
 *   DESCRIPTION: generate LC-3 assembly code for an for loop
 *   INPUTS: ast -- the AST node corresponding to the for loop
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*first check the initial condition expression, then check the test condition.
 Next, check the body statement and update and branch to test, it pass, go iteration, if no
 branch to end*/
static void
gen_for_statement (ast220_t* ast)
{
  ece220_label_t* target_label; /*label to target code*/
  ece220_label_t* pass; /*label for the true statement*/
  ece220_label_t* fail; /*label for the fail statement*/
  ece220_label_t* temp;/*a temporary label*/
  target_label = label_create();/*create label*/
  pass = label_create();/*create label*/
  fail = label_create();/*create label*/
  temp = label_create();/*create label*/
  if(ast->left != NULL)
   {
    gen_statement(ast->left); /*the initial condition*/
   }
  printf("%s\n", label_value(target_label)); /*target label*/
  gen_expression(ast->test); /*check the test expression*/
  /*test the result*/
  printf("\tADD R6, R6, #1\n"); /*pop the value*/
  printf("\tLDR R0, R6, #0\n"); /*check if it is true*/
  printf("\tADD R0, R0, #0\n");
  printf("\tBRnp %s\n", label_value(pass)); /*branch to statement code*/
  printf("\tLD R3, %s\n", label_value(temp)); /*branch to the code after for loop*/
  printf("\tJMP R3\n");
  printf("%s\n",label_value(temp));
  printf("\t.FILL %s\n", label_value(fail)); /*Fill value contain the fail label*/
  printf("%s\n", label_value(pass));/*label for if statement*/
  ast220_t** search; /*variable for traversal the linkedlist*/
  for(search = &(ast->middle); *search != NULL; search = &((*search)->next))
  {
    gen_statement(*search); /*traversal the if statement*/
  }
  if(ast->right != NULL)  /*check the update statement*/
  {
    gen_statement(ast->right); /*call update statement*/
  }
  gen_long_branch(7, target_label); /*branch to target label*/
  printf("%s\n", label_value(fail)); /*label for fail*/
}


/*
 * gen_if_statement
 *   DESCRIPTION: generate LC-3 assembly code for an if statement
 *   INPUTS: ast -- the AST node corresponding to the if statement
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*first check the test condition, if it is true go to the if statements
 if not go to the else statement*/
static void
gen_if_statement (ast220_t* ast)
{
    ece220_label_t* if_st;  /*label for if statement*/
    ece220_label_t* else_st;/*label for else statement*/
    ece220_label_t* temp;/*temporary label*/
    ece220_label_t* skip;/*label for skip the else statement*/
    ast220_t** search;/*double pointer to traversal*/

    if_st = label_create();/*create label*/
    else_st = label_create();/*create label*/
    temp = label_create();/*create label*/
    skip = label_create();/*create label*/
    gen_expression(ast->test);/*check the test statement*/
    printf("\tLDR R0, R6, #0\n");/*pop the value*/
    printf("\tADD R6, R6, #1\n");
    printf("\tADD R0, R0, #0\n");/*check if it is true*/
    printf("\tBRnp %s\n", label_value(if_st));/*if true branch to if statement*/
    printf("\tLD R3, %s\n", label_value(temp));/*branch to else statement*/
    printf("\tJMP R3\n");
    printf("%s\n", label_value(temp));
    printf("\t.FILL %s\n", label_value(else_st));
    printf("%s\n", label_value(if_st));/*label for if statement*/
    for(search = &(ast->left); *search != NULL; search = &((*search)->next))
    {
      gen_statement(*search);/*check the if statement*/
    }

    gen_long_branch(7, skip);/*skip else statement*/
    printf("%s\n", label_value(else_st));/*label for else statement*/
    for(search = &(ast->right); *search != NULL; search = &((*search)->next))
    {
      gen_statement(*search);/*check the else statement*/
    }
    printf("%s\n", label_value(skip));/*label for skip*/
}

/*ype ^ 7
 * gen_return_statement
 *   DESCRIPTION: generate LC-3 assembly code for a return statement
 *   INPUTS: ast -- the AST node corresponding to the return statement
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*check the expression and put it to return value in stack frame and
 branch to tear down code*/
static void
gen_return_statement (ast220_t* ast)
{
  ast220_t* ret = ast->left;
  gen_expression(ret);/*check the expression*/
  printf("\tLDR R0, R6, #0\n");/*pop the value*/
  printf("\tADD R6, R6, #1\n");
  printf("\tSTR R0, R5, #3\n");/*store the return value*/
  gen_long_branch(7, branch);/*branch to tear down code*/
}

/*
 * gen_pop_stack
 *   DESCRIPTION: generate LC-3 assembly code to pop and discard a value
 *                from the stack
 *   INPUTS: ast -- the AST node corresponding to the pop stack statement
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*check the expression and pop*/
static void
gen_pop_stack (ast220_t* ast)
{
  gen_expression(ast->left);/*check expression*/
  printf("\tADD R6, R6, #1\n");/*pop the value*/
}

/*
 * gen_debug_marker
 *   DESCRIPTION: generate LC-3 assembly code for a debug marker used to
 *                help debug LC-3 code generation; the marker is simply
 *                a comment in the assembly code that can be used to
 *                identify pieces of code generated by the compiler
 *   INPUTS: ast -- the AST node corresponding to the debug marker
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints an LC-3 assembly comment
 */
static void
gen_debug_marker (ast220_t* ast)
{
    printf ("; --------------- DEBUG(%d) ---------------\n", ast->value);
}

/*
 * gen_expression
 *   DESCRIPTION: generate LC-3 assembly code to calculate an arbitrary
 *                expression and push the result onto the stack
 *   INPUTS: ast -- the AST node corresponding to the expression
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
static void
gen_expression (ast220_t* ast)
{
    switch (ast->type) {
        case AST220_PUSH_INT:     gen_push_int (ast);       break;
        case AST220_PUSH_STR:     gen_push_str (ast);       break;
        case AST220_VARIABLE:     gen_push_variable (ast);  break;
        case AST220_FUNC_CALL:    gen_func_call (ast);      break;
	case AST220_GET_ADDRESS:  gen_get_address (ast);    break;
	case AST220_OP_ASSIGN:    gen_op_assign (ast);      break;
	case AST220_OP_PRE_INCR:  gen_op_pre_incr (ast);    break;
	case AST220_OP_PRE_DECR:  gen_op_pre_decr (ast);    break;
	case AST220_OP_POST_INCR: gen_op_post_incr (ast);   break;
	case AST220_OP_POST_DECR: gen_op_post_decr (ast);   break;
	case AST220_OP_ADD:       gen_op_add (ast);         break;
	case AST220_OP_SUB:       gen_op_sub (ast);         break;
	case AST220_OP_MULT:      gen_op_mult (ast);        break;
	case AST220_OP_DIV:       gen_op_div (ast);         break;
	case AST220_OP_MOD:       gen_op_mod (ast);         break;
	case AST220_OP_NEGATE:    gen_op_negate (ast);      break;
	case AST220_OP_LOG_NOT:   gen_op_log_not (ast);     break;
	case AST220_OP_LOG_OR:    gen_op_log_or (ast);      break;
	case AST220_OP_LOG_AND:   gen_op_log_and (ast);     break;
	case AST220_CMP_NE:       gen_op_cmp_ne (ast);      break;
	case AST220_CMP_LESS:     gen_op_cmp_less (ast);    break;
	case AST220_CMP_LE:       gen_op_cmp_le (ast);      break;
	case AST220_CMP_EQ:       gen_op_cmp_eq (ast);      break;
	case AST220_CMP_GE:       gen_op_cmp_ge (ast);      break;
	case AST220_CMP_GREATER:  gen_op_cmp_greater (ast); break;
	default: fputs ("BAD EXPRESSION TYPE\n", stderr);   break;
    }
}

/*
 * gen_push_int
 *   DESCRIPTION: generate LC-3 assembly code to push a constant integer
 *                expression onto the stack
 *   INPUTS: ast -- the AST node corresponding to the integer
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*use a label to load the value and store in stack*/
static void
gen_push_int (ast220_t* ast)
{
  ece220_label_t* target_label;/*label for target*/
  ece220_label_t* br_label;/*branch label*/
  target_label = label_create();/*create label*/
  br_label = label_create();/*create label*/
  printf("\tLD R0, %s\n", label_value(target_label));/*load the value*/
  printf("\tADD R6, R6, #-1\n");/*decreament the stack pointer*/
  printf("\tSTR R0, R6, #0\n");/*push the value to the stack*/
  printf("\tBRnzp %s\n", label_value(br_label));/*branch to branch label*/
  printf("%s\n", label_value(target_label));/*target_label*/
  printf("\t.FILL #%d\n", ast->value);/*fill the value*/
  printf("%s\n", label_value(br_label));/*branch label*/
}

/*
 * gen_push_str
 *   DESCRIPTION: generate LC-3 assembly code to push a constant string
 *                expression onto the stack
 *   INPUTS: ast -- the AST node corresponding to the string
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*use a label to load the string and load the address to stack*/
static void
gen_push_str (ast220_t* ast)
{
  ece220_label_t* target_label;/*label for target*/
  ece220_label_t* br_label;/*create a branch label*/
  target_label = label_create();/*create the label*/
  br_label = label_create();/*create the label*/
  printf("\tLEA R0, %s\n", label_value(target_label));/*load the address of the first letter*/
  printf("\tADD R6, R6, #-1\n");/*decreament the stack pointer*/
  printf("\tSTR R0, R6, #0\n");/*store the address to the stack*/
  printf("\tBRnzp %s\n", label_value(br_label));/*branch to branch label*/
  printf("%s\n", label_value(target_label));/*target_label*/
  printf("\t.STRINGZ %s\n", ast->name);/*fill the string*/
  printf("%s\n", label_value(br_label));/*branch label*/
}

/*
 * gen_push_variable
 *   DESCRIPTION: generate LC-3 assembly code to push a variable's value
 *                onto the stack
 *   INPUTS: ast -- the AST node corresponding to the variable reference
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*first check it is array or scalar and then check if it is global and then
 check the address and push the value to the stack*/
static void
gen_push_variable (ast220_t* ast)
{
    symtab_entry_t* symtab = symtab_lookup(ast->name);/*create pointer for symbal tabel*/
    /*global or local*/
      if(ast->left == NULL)/*check if it is array*/
      {
          if(1 == symtab->is_global)/*check if it is global*/
          {
          printf("\tLDR R0, R4, #%d\n", symtab->offset);/*load the value*/
          }
          else
          {
          printf("\tLDR R0, R5, #%d\n", symtab->offset);/*load the value*/
          }
          printf("\tADD R6, R6, #-1\n");/*decreament the stack pointer*/
          printf("\tSTR R0, R6, #0\n");/*push the variable*/
      }
      else
      {
          gen_expression(ast->left);/*calculate the index of the array*/
          printf("\tLDR R0, R6, #0\n");/*pop the value*/
          printf("\tADD R6, R6, #1\n");
          if(1 == symtab->is_global)/*check if it is global*/
          {
          printf("\tADD R1, R4, #%d\n", symtab->offset);/*load the value*/
          }
          else
          {
          printf("\tADD R1, R5, #%d\n", symtab->offset);/*load the value*/
          }
          printf("\tADD R0, R0, R1\n");/*find the index in the stack frame*/
          printf("\tLDR R2, R0, #0\n");/*load the value*/
          printf("\tADD R6, R6, #-1\n");/*decreament the stack pointer*/
          printf("\tSTR R2, R6, #0\n");/*push the array*/
      }
}

/*
 * gen_func_call
 *   DESCRIPTION: generate LC-3 assembly code to perform a function call,
 *                remove the arguments from the stack, and leave the
 *                return value on top of the stack
 *   INPUTS: ast -- the AST node corresponding to the function call
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*first find all the body statement and then check which function we
 need to call according to the fnum and pop the parameter and push return value*/
static void
gen_func_call (ast220_t* ast)
{
    ast220_t** trav;/*traversal the expression*/
    int i = 0;/*check the parameter*/
    for(trav = &(ast->left) ; *trav != NULL; trav = &((*trav)->next))
      {
        gen_expression(*trav);/*check expression*/
        i++;/*increament the parameter*/
      }
    ece220_label_t* target_label;/*label for the target*/
    ece220_label_t* br_label;/*brach label*/
    target_label = label_create();/*create label*/
    br_label = label_create();/*create label*/
    printf("\tLD R0, %s\n", label_value(target_label));/*load the function to R0*/
    printf("\tJSRR R0\n");/*call function*/
    printf("\tBRnzp %s\n", label_value(br_label));/*branch to brach label*/
    printf("%s\n", label_value(target_label));
    if(ast->fnum == 0)/*check the function number*/
    {
      printf("\t.FILL PRINTF\n");
    }
    else if(ast->fnum == 1)
    {
      printf("\t.FILL RAND\n");
    }
    else if(ast->fnum == 2)
    {
      printf("\t.FILL SCANF\n");
    }
    else if(ast->fnum == 3)
    {
      printf("\t.FILL SRAND\n");
    }
    printf("%s\n", label_value(br_label));/*branch label*/
    printf("\tLDR R0, R6, #0\n");/*pop the value*/
    printf("\tADD R6, R6, #1\n");
    printf("\tADD R6, R6, #%d\n", i);/*pop the parameters*/
    printf("\tADD R6, R6, #-1\n");/*decreament the stack pointer*/
    printf("\tSTR R0, R6, #0\n");/*push the return value*/
}

/*
 * gen_get_address
 *   DESCRIPTION: generate LC-3 assembly code to push the address of
 *                a variable onto the stack
 *   INPUTS: ast -- the AST node corresponding to the variable reference
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*first check it is array or scalar and then check if it is global and then
 check the address and push to stack*/
static void
gen_get_address (ast220_t* ast)
{
  symtab_entry_t* symtab = symtab_lookup(ast->left->name);/*symbal tabel pointer*/
  if(ast->left->left == NULL)/*check if it is array*/
  {
    if(1 == symtab->is_global)/*check if it is global*/
    {
    printf("\tADD R0, R4, #%d\n", symtab->offset);/*find the address*/
    }
    else
    {
    printf("\tADD R0, R5, #%d\n", symtab->offset);/*load the address*/
    }
    printf("\tADD R6, R6, #-1\n");/*decreament the stack pointer*/
    printf("\tSTR R0, R6, #0\n");/*push to the stack*/
  }
  else
  {
    gen_expression(ast->left->left);/*find the index*/
    printf("\tLDR R2, R6, #0\n");/*pop the value*/
    printf("\tADD R6, R6, #1\n");
    if(1 == symtab->is_global)
    {
    printf("\tADD R0, R4, #%d\n", symtab->offset)/*find the address of array*/;
    }
    else
    {
    printf("\tADD R0, R5, #%d\n", symtab->offset);/*fidn the address of the array*/
    }
    printf("\tADD R0, R0, R2\n");/*find the address of the element*/
    printf("\tADD R6, R6, #-1\n");/*decreament the stack pointer*/
    printf("\tSTR R0, R6, #0\n");/*push to the stack*/
  }
}

/*
 * gen_op_assign
 *   DESCRIPTION: generate LC-3 assembly code to perform an assignment,
 *                leaving the value assigned on the stack (assignments
 *                are also expressions, with value equal to that of the
 *                value assigned)
 *   INPUTS: ast -- the AST node corresponding to the assignment
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*first call the expression and check it is array or scalar and then check if it is global and then
 check the address and push to that address*/
static void
gen_op_assign (ast220_t* ast)
{
  ast220_t*  expr= ast-> right;
  gen_expression(expr);/*check the expression*/
  symtab_entry_t* symtab = symtab_lookup(ast->left->name);/*symbal tabel pointer*/
  if(ast->left->left == NULL)/*check if it is array*/
  {
    if(1 == symtab->is_global)/*check if it is global*/
    {
    printf("\tADD R0, R4, #%d\n", symtab->offset);/*find the address*/
    }
    else
    {
    printf("\tADD R0, R5, #%d\n", symtab->offset);/*find the address*/
    }
    printf("\tLDR R1, R6, #0\n");/*load the value to R1*/
    printf("\tSTR R1, R0, #0\n");/*store in R0*/
  }
  else
  {
    gen_expression(ast->left->left);/*check the index*/
    printf("\tLDR R2, R6, #0\n");/*pop the value*/
    printf("\tADD R6, R6, #1\n");
    if(1 == symtab->is_global)/*check if it is global*/
    {
    printf("\tADD R0, R4, #%d\n", symtab->offset);/*find the address*/
    }
    else
    {
    printf("\tADD R0, R5, #%d\n", symtab->offset);/*find the address*/
    }
    printf("\tADD R0, R0, R2\n");/*find the address of the element*/
    printf("\tLDR R1, R6, #0\n");/*load the value*/
    printf("\tSTR R1, R0, #0\n");/*store in R0*/
  }
}

/*
 * gen_op_pre_incr
 *   DESCRIPTION: generate LC-3 assembly code to for a pre-increment
 *                expression, which increments a variable and pushes
 *                the new value of the variable onto the stack
 *   INPUTS: ast -- the AST node corresponding to pre-increment
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*first check it is array or scalar and then check if it is global and then
 check the address and laod the value and increment. put the value to stack and
 address*/
static void
gen_op_pre_incr (ast220_t* ast)
{
  symtab_entry_t* symtab = symtab_lookup(ast->left->name);/*symbal tabel pointer*/
  if(ast->left->left == NULL)/*check if it is array*/
  {
    if(1 == symtab->is_global)/*check if it is global*/
    {
    printf("\tADD R0, R4, #%d\n", symtab->offset);/*find the address*/
    }
    else
    {
    printf("\tADD R0, R5, #%d\n", symtab->offset);/*find the address*/
    }
    printf("\tLDR R1, R0, #0\n");/*pop the value*/
    printf("\tADD R1, R1, #1\n");/*increment*/
    printf("\tSTR R1, R0, #0\n");/*store in stack frame*/
    printf("\tADD R6, R6, #-1\n");/*push to stack*/
    printf("\tSTR R1, R6, #0\n");
  }
  else
  {
    gen_expression(ast->left->left);/*find the index*/
    printf("\tLDR R0, R6, #0\n");/*pop the value*/
    printf("\tADD R6, R6, #1\n");
    if(1 == symtab->is_global)/*find it it is global*/
    {
    printf("\tADD R1, R4, #%d\n", symtab->offset);/*find the address*/
    }
    else
    {
    printf("\tADD R1, R5, #%d\n", symtab->offset);/*find the address*/
    }
    printf("\tADD R0, R0, R1\n");/*chedck the address of the element*/
    printf("\tLDR R2, R0, #0\n");/*load the value*/
    printf("\tADD R2, R2, #1\n");/*increment*/
    printf("\tSTR R2, R0, #0\n");/*push to stack frame*/
    printf("\tADD R6, R6, #-1\n");/*push to stack*/
    printf("\tSTR R2, R6, #0\n");
  }
}

/*
 * gen_op_pre_decr
 *   DESCRIPTION: generate LC-3 assembly code to for a pre-decrement
 *                expression, which decrements a variable and pushes
 *                the new value of the variable onto the stack
 *   INPUTS: ast -- the AST node corresponding to pre-decrement
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*first check it is array or scalar and then check if it is global and then
 check the address and laod the value and decreament. put the value to stack and
 address*/
static void
gen_op_pre_decr (ast220_t* ast)
{
  symtab_entry_t* symtab = symtab_lookup(ast->left->name);/*check the symbal tabel*/
  if(ast->left->left == NULL)/*check if it is array*/
  {
    if(1 == symtab->is_global)/*check if it is global*/
    {
    printf("\tADD R0, R4, #%d\n", symtab->offset);/*find the address*/
    }
    else
    {
    printf("\tADD R0, R5, #%d\n", symtab->offset);/*find the address*/
    }
    printf("\tLDR R1, R0, #0\n");/*load the value*/
    printf("\tADD R1, R1, #-1\n");/*decreament*/
    printf("\tSTR R1, R0, #0\n");/*push to stack frame*/
    printf("\tADD R6, R6, #-1\n");/*push to stack*/
    printf("\tSTR R1, R6, #0\n");
  }
  else
  {
    gen_expression(ast->left->left);/*find the index*/
    printf("\tLDR R0, R6, #0\n");/*pop the value*/
    printf("\tADD R6, R6, #1\n");
    if(1 == symtab->is_global)/*find it if if global*/
    {
    printf("\tADD R1, R4, #%d\n", symtab->offset);/*find the address*/
    }
    else
    {
    printf("\tADD R1, R5, #%d\n", symtab->offset);/*find the address*/
    }
    printf("\tADD R0, R0, R1\n");/*find the address of the element*/
    printf("\tLDR R2, R0, #0\n");/*load the value*/
    printf("\tADD R2, R2, #-1\n");/*decrement*/
    printf("\tSTR R2, R0, #0\n");/*push to stack frame*/
    printf("\tADD R6, R6, #-1\n");/*push to stack*/
    printf("\tSTR R2, R6, #0\n");
  }
}

/*
 * gen_op_post_incr
 *   DESCRIPTION: generate LC-3 assembly code to for a post-increment
 *                expression, which increments a variable and pushes
 *                the original value of the variable onto the stack
 *   INPUTS: ast -- the AST node corresponding to post-increment
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*first check it is array or scalar and then check if it is global and then
 check the address and laod the value and increment. put the original value
  to stack and new value to address*/
static void
gen_op_post_incr (ast220_t* ast)
{
  symtab_entry_t* symtab = symtab_lookup(ast->left->name);/*symbal tabel pointer*/
  if(ast->left->left == NULL)/*check if it is array*/
  {
    if(1 == symtab->is_global)/*check if it is global*/
    {
    printf("\tADD R0, R4, #%d\n", symtab->offset);/*find the address*/
    }
    else
    {
    printf("\tADD R0, R5, #%d\n", symtab->offset);/*find the address*/
    }
    printf("\tLDR R1, R0, #0\n");/*load the value*/
    printf("\tADD R2, R1, #1\n");/*decrement*/
    printf("\tSTR R2, R0, #0\n");/*store in stack frame*/
    printf("\tADD R6, R6, #-1\n");/*push to stack*/
    printf("\tSTR R1, R6, #0\n");
  }
  else
  {
    gen_expression(ast->left->left);/*find the index*/
    printf("\tLDR R0, R6, #0\n");/*pop the value*/
    printf("\tADD R6, R6, #1\n");
    if(1 == symtab->is_global)/*check if it is global*/
    {
    printf("\tADD R1, R4, #%d\n", symtab->offset);/*find the address*/
    }
    else
    {
    printf("\tADD R1, R5, #%d\n", symtab->offset);/*find the address*/
    }
    printf("\tADD R0, R0, R1\n");/*find the address of the element*/
    printf("\tLDR R2, R0, #0\n");/*load the value*/
    printf("\tADD R3, R2, #1\n");/*increment*/
    printf("\tSTR R3, R0, #0\n");/*store the value in stack frame*/
    printf("\tADD R6, R6, #-1\n");/*push the original value to stack*/
    printf("\tSTR R2, R6, #0\n");
  }
}

/*
 * gen_op_post_decr
 *   DESCRIPTION: generate LC-3 assembly code to for a post-decrement
 *                expression, which decrements a variable and pushes
 *                the original value of the variable onto the stack
 *   INPUTS: ast -- the AST node corresponding to post-decrement
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*first check it is array or scalar and then check if it is global and then
 check the address and laod the value and decreament. put the original value
  to stack and new value to address*/
static void
gen_op_post_decr (ast220_t* ast)
{
  symtab_entry_t* symtab = symtab_lookup(ast->left->name);/*symbal tabel pointer*/
  if(ast->left->left == NULL)/*check if it is array*/
  {
    if(1 == symtab->is_global)/*check if it is global*/
    {
    printf("\tADD R0, R4, #%d\n", symtab->offset);/*find the address*/
    }
    else
    {
    printf("\tADD R0, R5, #%d\n", symtab->offset);/*find the address*/
    }
    printf("\tLDR R1, R0, #0\n");/*load the value*/
    printf("\tADD R2, R1, #-1\n");/*decrement*/
    printf("\tSTR R2, R0, #0\n");/*store the value in stack frame*/
    printf("\tADD R6, R6, #-1\n");/*push the original value in stack*/
    printf("\tSTR R1, R6, #0\n");
  }
  else
  {
    gen_expression(ast->left->left);/*check the index*/
    printf("\tLDR R0, R6, #0\n");/*pop the value*/
    printf("\tADD R6, R6, #1\n");
    if(1 == symtab->is_global)/*check if it is global*/
    {
    printf("\tADD R1, R4, #%d\n", symtab->offset);/*find the address*/
    }
    else
    {
    printf("\tADD R1, R5, #%d\n", symtab->offset);/*find the address*/
    }
    printf("\tADD R0, R0, R1\n");/*find the address of the element*/
    printf("\tLDR R2, R0, #0\n");/*load the value*/
    printf("\tADD R3, R2, #-1\n");/*decreament*/
    printf("\tSTR R3, R0, #0\n");/*store the value to stack frame*/
    printf("\tADD R6, R6, #-1\n");/*push the original value to stack*/
    printf("\tSTR R2, R6, #0\n");
  }
}

/*
 * gen_op_add
 *   DESCRIPTION: generate LC-3 assembly code to calculate the sum of two
 *                expressions, leaving the sum on the stack
 *   INPUTS: ast -- the AST node corresponding to the add operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*check the left opreand and right oprand and then add together*/
static void
gen_op_add (ast220_t* ast)
{
  ast220_t* adlf = ast->left;/*check the left operand*/
  gen_expression(adlf);
  ast220_t* adrt = ast->right;/*check the right operand*/
  gen_expression(adrt);
  printf("\tLDR R0, R6, #0\n");/*pop the right operand*/
  printf("\tADD R6, R6, #1\n");
  printf("\tLDR R1, R6, #0\n");/*pop the left operand*/
  printf("\tADD R6, R6, #1\n");
  printf("\tADD R0, R0, R1\n");/*add together*/
  printf("\tADD R6, R6, #-1\n");/*push to stack*/
  printf("\tSTR R0, R6, #0\n");
}

/*
 * gen_op_sub
 *   DESCRIPTION: generate LC-3 assembly code to calculate the difference
 *                of two expressions, leaving the difference on the stack
 *   INPUTS: ast -- the AST node corresponding to the subtraction operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*check the left opreand and right oprand and then subtract*/
static void
gen_op_sub (ast220_t* ast)
{
  ast220_t* sublf = ast->left;/*check the left operand*/
  gen_expression(sublf);
  ast220_t* subrt = ast->right;/*check the right operand*/
  gen_expression(subrt);
  printf("\tLDR R0, R6, #0\n");/*pop the right operand*/
  printf("\tADD R6, R6, #1\n");
  printf("\tLDR R1, R6, #0\n");/*pop the left operand*/
  printf("\tADD R6, R6, #1\n");
  printf("\tNOT R0, R0\n");/*negate right*/
  printf("\tADD R0, R0, #1\n");
  printf("\tADD R0, R0, R1\n");/*add together*/
  printf("\tADD R6, R6, #-1\n");/*push to stack*/
  printf("\tSTR R0, R6, #0\n");
}

/*
 * gen_op_mult
 *   DESCRIPTION: generate LC-3 assembly code to calculate the product
 *                of two expressions (using the MULTIPLY subroutine in
 *                the LC-3 library), leaving the product on the stack
 *   INPUTS: ast -- the AST node corresponding to the multiplication operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*check the left opreand and right oprand and then call MULTIPLY subroutine and
 push result to stack*/
static void
gen_op_mult (ast220_t* ast)
{
    gen_expression(ast->left);/*check the left operand*/
    gen_expression(ast->right);/*check the right operand*/
    ece220_label_t* target_label;/*create target label*/
    ece220_label_t* br_label;/*create target label*/
    target_label = label_create();
    br_label = label_create();
    printf("\tLDR R0, R6, #0\n");/*pop the right operand*/
    printf("\tADD R6, R6, #1\n");
    printf("\tLDR R1, R6, #0\n");/*pop the left operand*/
    printf("\tADD R6, R6, #1\n");
    printf("\tLD R2, %s\n", label_value(target_label));/*call MULTIPLY*/
    printf("\tJSRR R2\n");
    printf("\tBRnzp %s\n", label_value(br_label));
    printf("%s\n", label_value(target_label));
    printf("\t.FILL MULTIPLY\n");
    printf("%s\n", label_value(br_label));
    printf("\tADD R6, R6, #-1\n");/*push the value*/
    printf("\tSTR R0, R6, #0\n");
}

/*
 * gen_op_div
 *   DESCRIPTION: generate LC-3 assembly code to calculate the quotient
 *                of two expressions (using the DIVIDE subroutine in
 *                the LC-3 library), leaving the quotient on the stack
 *   INPUTS: ast -- the AST node corresponding to the division operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*check the left opreand and right oprand and then call DIVIDE subroutine and
 push result to stack*/
static void
gen_op_div (ast220_t* ast)
{
    gen_expression(ast->left);/*check the left operand*/
    gen_expression(ast->right);/*check the right operand*/
    ece220_label_t* target_label;/*create target label*/
    ece220_label_t* br_label;/*create branch label*/
    target_label = label_create();
    br_label = label_create();
    printf("\tLDR R1, R6, #0\n");/*pop the right operand*/
    printf("\tADD R6, R6, #1\n");
    printf("\tLDR R0, R6, #0\n");/*pop the left operand*/
    printf("\tADD R6, R6, #1\n");
    printf("\tLD R2, %s\n", label_value(target_label));/*call DIVIDE*/
    printf("\tJSRR R2\n");
    printf("\tBRnzp %s\n", label_value(br_label));
    printf("%s\n", label_value(target_label));
    printf("\t.FILL DIVIDE\n");
    printf("%s\n", label_value(br_label));
    printf("\tADD R6, R6, #-1\n");/*push the value*/
    printf("\tSTR R0, R6, #0\n");
}

/*
 * gen_op_mod
 *   DESCRIPTION: generate LC-3 assembly code to calculate the modulus
 *                of one expression relative to a second expression (using
 *                the MODULUS subroutine in the LC-3 library), leaving
 *                the result on the stack
 *   INPUTS: ast -- the AST node corresponding to the division operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*check the left opreand and right oprand and then call MODULUS subroutine and
 push result to stack*/
static void
gen_op_mod (ast220_t* ast)
{
    gen_expression(ast->left);/*check the left operand*/
    gen_expression(ast->right);/*check the right operand*/
    ece220_label_t* target_label;/*create the target label*/
    ece220_label_t* br_label;/*create the branch label*/
    target_label = label_create();
    br_label = label_create();
    printf("\tLDR R1, R6, #0\n");/*pop the right operand*/
    printf("\tADD R6, R6, #1\n");
    printf("\tLDR R0, R6, #0\n");/*pop the left operand*/
    printf("\tADD R6, R6, #1\n");
    printf("\tLD R2, %s\n", label_value(target_label));/*call MODULUS*/
    printf("\tJSRR R2\n");
    printf("\tBRnzp %s\n", label_value(br_label));
    printf("%s\n", label_value(target_label));
    printf("\t.FILL MODULUS\n");
    printf("%s\n", label_value(br_label));
    printf("\tADD R6, R6, #-1\n");/*push the value*/
    printf("\tSTR R0, R6, #0\n");
}

/*
 * gen_op_negate
 *   DESCRIPTION: generate LC-3 assembly code to negate the value of an
 *                expression, leaving the result on the stack
 *   INPUTS: ast -- the AST node corresponding to the negation operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*get the expression and negate*/
static void
gen_op_negate (ast220_t* ast)
{
  ast220_t* neg = ast->left;
  gen_expression(neg);/*check the operation*/
  printf("\tLDR R0, R6, #0\n");/*pop the value*/
  printf("\tADD R6, R6, #1\n");
  printf("\tNOT R0, R0\n");/*not the value and add 1*/
  printf("\tADD R0, R0, #1\n");
  printf("\tADD R6, R6, #-1\n");/*push to stack*/
  printf("\tSTR R0, R6, #0\n");
}

/*
 * gen_op_log_not
 *   DESCRIPTION: generate LC-3 assembly code to perform a logical NOT
 *                operation on an expression, leaving the result (0 or 1)
 *                on the stack
 *   INPUTS: ast -- the AST node corresponding to the logical NOT operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*find the expression and then check it is 0 or 1 and then negate and
 store in stack*/
static void
gen_op_log_not (ast220_t* ast)
{
  ece220_label_t* target_label;/*create label for target*/
  target_label = label_create();
  gen_expression(ast->left);/*check expression*/
  printf("\tLDR R0, R6, #0\n");/*pop the value*/
  printf("\tADD R6, R6, #1\n");
  printf("\tAND R1, R1, #0\n");/*clear R1*/
  printf("\tADD R0, R0, #0\n");/*check if R0 is positive*/
  printf("\tBRnp %s\n", label_value(target_label));/*if yes, branch to target*/
  printf("\tADD R1, R1, #1\n");/*increament R1*/
  printf("%s\n", label_value(target_label));
  printf("\tADD R6, R6, #-1\n");/*push R1 to stack*/
  printf("\tSTR R1, R6, #0\n");
}

/*
 * gen_op_log_or
 *   DESCRIPTION: generate LC-3 assembly code to perform a logical OR
 *                operation on two expressions, leaving the result (0 or 1)
 *                on the stack; the code generated must perform proper
 *                shortcutting, i.e., if the first expression is true
 *                the second is not evaluated (the code is not executed)
 *   INPUTS: ast -- the AST node corresponding to the logical OR operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*check the first expression if it is positive, skip the remaining expression and store 1
 to stack, if it is zero, check second expression if 0 store 0 to stack*/
static void
gen_op_log_or (ast220_t* ast)
{
  ece220_label_t* target_label;/*create the target_label*/
  ece220_label_t* false_label;/*create false_label*/
  ece220_label_t* end;/*create the label for end*/
  target_label = label_create();
  false_label = label_create();
  end = label_create();
  gen_expression(ast->left);/*check the left expression*/
  printf("\tLDR R0, R6, #0\n");/*pop the value*/
  printf("\tADD R6, R6, #1\n");
  printf("\tADD R0, R0, #0\n");/*check if it is zero*/
  printf("\tBRz %s\n", label_value(false_label));/*if yes branch to next expression*/
  gen_long_branch(7, target_label);/*if it is positive branch to target_label, shortcut*/
  printf("%s\n", label_value(false_label));
  gen_expression(ast->right);/*check the second expression*/
  printf("\tLDR R0, R6, #0\n");/*pop the value*/
  printf("\tADD R6, R6, #1\n");
  printf("\tADD R0, R0, #0\n");/*check if it is zero*/
  printf("\tBRnp %s\n", label_value(target_label));/*if it is positive, branch to target*/
  printf("\tAND R1, R1, #0\n");/*clear R1*/
  printf("\tBRnzp %s\n", label_value(end));/*branch to end*/
  printf("%s\n", label_value(target_label));/*target_label*/
  printf("\tAND R1, R1, #0\n");/*clear R1 and increment by 1*/
  printf("\tADD R1, R1, #1\n");
  printf("%s\n", label_value(end));/*end label*/
  printf("\tADD R6, R6, #-1\n");/*push R1 to stack*/
  printf("\tSTR R1, R6, #0\n");
}

/*
 * gen_op_log_and
 *   DESCRIPTION: generate LC-3 assembly code to perform a logical AND
 *                operation on two expressions, leaving the result (0 or 1)
 *                on the stack; the code generated must perform proper
 *                shortcutting, i.e., if the first expression is false
 *                the second is not evaluated (the code is not executed)
 *   INPUTS: ast -- the AST node corresponding to the logical AND operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
 /*check the first expression if it is 0, skip the remaining expression and store 0
 to stack, if it is 1, check second expression if 1 store 1 to stack, if 0 store 0*/
static void
gen_op_log_and (ast220_t* ast)
{
  ece220_label_t* target_label;/*create target_label*/
  ece220_label_t* false_label;/*create false_label*/
  ece220_label_t* end;/*create end label*/
  target_label = label_create();
  false_label = label_create();
  end = label_create();
  gen_expression(ast->left);/*check the first expression*/
  printf("\tLDR R0, R6, #0\n");/*pop the value*/
  printf("\tADD R6, R6, #1\n");
  printf("\tADD R0, R0, #0\n");/*check if it is positive*/
  printf("\tBRnp %s\n", label_value(target_label));/*if yes, check second expression*/
  gen_long_branch(7, false_label);/*branch to false label if it is zero*/
  printf("%s\n", label_value(target_label));
  gen_expression(ast->right);/*check the second expression*/
  printf("\tLDR R0, R6, #0\n");/*pop the value*/
  printf("\tADD R6, R6, #1\n");
  printf("\tADD R0, R0, #0\n");/*check if it is zero*/
  printf("\tBRz %s\n", label_value(false_label));/*if it is zero, branch to false label*/
  printf("\tAND R1, R1, #0\n");/*clear R1 and increment by 1*/
  printf("\tADD R1, R1, #1\n");
  printf("\tBRnzp %s\n", label_value(end));/*branch to end*/
  printf("%s\n", label_value(false_label));/*false label*/
  printf("\tAND R1, R1, #0\n");/*clear R1*/
  printf("%s\n", label_value(end));/*end label*/
  printf("\tADD R6, R6, #-1\n");/*push R1 to stack*/
  printf("\tSTR R1, R6, #0\n");
}

/*
 * gen_comparison
 *   DESCRIPTION: generate LC-3 assembly code for a comparison operator,
 *                leaving the result (0 or 1) on the stack
 *   INPUTS: ast -- the AST node corresponding to the comparison
 *           false_cond -- a string representation of the condition codes
 *                         for which the comparison is false (as calculated
 *                         by subtracting the second expression from the
 *                         first)
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 *   KNOWN BUGS: ignores 2's complement overflow in making the comparison
 */
static void
gen_comparison (ast220_t* ast, const char* false_cond)
{
    ece220_label_t* false_label;

    false_label = label_create ();
    gen_expression (ast->left);
    gen_expression (ast->right);
    printf ("\tLDR R1,R6,#0\n\tLDR R0,R6,#1\n\tADD R6,R6,#2\n");
    printf ("\tAND R2,R2,#0\n\tNOT R1,R1\n\tADD R1,R1,#1\n\tADD R0,R0,R1\n");
    printf ("\tBR%s %s\n\tADD R2,R2,#1\n", false_cond,
	    label_value (false_label));
    printf ("%s\n", label_value (false_label));
    printf ("\tADD R6,R6,#-1\n\tSTR R2,R6,#0\n");
}

/*
 * gen_op_cmp_ne
 *   DESCRIPTION: generate LC-3 assembly code to compare whether the value
 *                of one expression is not equal to the value of a second
 *                expression, leaving the result (0 or 1) on the stack
 *   INPUTS: ast -- the AST node corresponding to the inequality operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
static void
gen_op_cmp_ne (ast220_t* ast)
{
    gen_comparison (ast, "z");
}

/*
 * gen_op_cmp_less
 *   DESCRIPTION: generate LC-3 assembly code to compare whether the value
 *                of one expression is less than the value of a second
 *                expression, leaving the result (0 or 1) on the stack
 *   INPUTS: ast -- the AST node corresponding to the less-than operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
static void
gen_op_cmp_less (ast220_t* ast)
{
    gen_comparison (ast, "zp");
}

/*
 * gen_op_cmp_le
 *   DESCRIPTION: generate LC-3 assembly code to compare whether the value
 *                of one expression is less than or equal to the value
 *                of a second expression, leaving the result (0 or 1) on
 *                the stack
 *   INPUTS: ast -- the AST node corresponding to the less-or-equal-to
 *                  operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
static void
gen_op_cmp_le (ast220_t* ast)
{
    gen_comparison (ast, "p");
}

/*
 * gen_op_cmp_eq
 *   DESCRIPTION: generate LC-3 assembly code to compare whether the value
 *                of one expression is equal to the value of a second
 *                expression, leaving the result (0 or 1) on the stack
 *   INPUTS: ast -- the AST node corresponding to the equality operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
static void
gen_op_cmp_eq (ast220_t* ast)
{
    gen_comparison (ast, "np");
}

/*
 * gen_op_cmp_ge
 *   DESCRIPTION: generate LC-3 assembly code to compare whether the value
 *                of one expression is greater than or equal to the value
 *                of a second expression, leaving the result (0 or 1) on
 *                the stack
 *   INPUTS: ast -- the AST node corresponding to the greater-or-equal-to
 *                  operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
static void
gen_op_cmp_ge (ast220_t* ast)
{
    gen_comparison (ast, "n");
}

/*
 * gen_op_cmp_greater
 *   DESCRIPTION: generate LC-3 assembly code to compare whether the value
 *                of one expression is greater than the value of a second
 *                expression, leaving the result (0 or 1) on the stack
 *   INPUTS: ast -- the AST node corresponding to the greater-than operation
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECTS: prints LC-3 instructions
 */
static void
gen_op_cmp_greater (ast220_t* ast)
{
    gen_comparison (ast, "nz");
}
