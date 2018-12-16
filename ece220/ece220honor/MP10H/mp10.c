#include <stdint.h>
#include <stdio.h>

#include "mp10.h"
//help function, calculate the power of 4
static int32_t
power(int32_t base, int32_t p)
{
  int i; //temp variable
  int result = 1;//the result
  for(i = 0; i<p; i++)//calculate the power
  {
    result = base*result;
  }
  // printf("%d\n", result);
  return result;//return the result
}
/*check if the vertex is less than 64, if not, calculate which level are there vertex stay
and then use seperate the node at that level into 64 part and find their ancestor in 4-level*/
int32_t
mark_vertex_minimap (graph_t* g, pyr_tree_t* p)
{  //temperary variable
  int num;//how many node in that level
  int first_leaf= p->n_nodes - g->n_vertices;;//find the first index of vertex in tree;
  int last_leaf = p->n_nodes -1;//last leaf index;
  int level = 5; //level variable;
  int level_last; //level at which last vertex in;
  int part; // divide the node at that level by 64 part
  int bit; //mm_bit
  int j; //temperary variable
  int index; //index value;
  int sum;
  //if vertex less than 64
      //calculate which level is first vertex in
      while((1-1*power(4, level))/(1-4) < first_leaf)
        {
          level++;
        }
      //calcylate which level is last vertex in;
      level_last = level;
      while(((1-1*power(4, level_last))/(1-4) < last_leaf))
        {
          level_last++;
        }
      //divide the node of that level by 64 part
      //calculate how many node in that level;
        num = power(4, level - 1);
        part = num / 64; //divide into 64 part
        sum = (1-1*power(4, level-1))/(1-4);
          bit = (first_leaf-sum)/part; //calculate the mm_bit for first vertex;
          j = (first_leaf-sum)%part; //calculate the initial value of j
          index = first_leaf; //initialize index value
          while(bit < 64) //for the vertex in the upper level
          {
            while(j< part)
            {
              (g->vertex)[(p->node)[index].id].mm_bit = bit; //fill the mm_bit value;
              index++;  //increament index;
              j++; //increament j;
            }
            j=0;
            bit ++;
          }
          //last level;
          num = power(4, level_last-1); //calculate the number of node  should in last level
          part= num/64; //how many node are in 1 part
          j = 0;
          for(bit = 0; bit <64 && index<= last_leaf; bit++) //loop end until we fill all vertex
          {
            while(j<part && index <= last_leaf) //loop end until we fill all vertex
              {
                (g->vertex)[(p->node)[index].id].mm_bit = bit; //fill the mm_bit value
                index++; //increament index
                j++;//increament j
              }
              j =0;
          }
          return 1;
}

/*find the mm_bit in that level and then shift 1 for mm_bti times */
void
build_vertex_set_minimap (graph_t* g, vertex_set_t* vs)
{
  //printf("lll\n");
  unsigned long long n= 0; //set a value n
  int i; //temperary variable
  int index; //index variable
  int shift; //how many bit should we shift
  for(i = 0; i < vs->count; i++ )
  {
    index = (vs->id)[i]; //the index of that vertex
    shift = (g->vertex)[index].mm_bit; //shift mm_bit times
    n |= (1ULL << (63-shift)); //shift and ORing together with old valye
  }
  vs->minimap = n;//fill minimap
}

/*find the mm_bit in that level and then shift 1 for mm_bti times */
void
build_path_minimap (graph_t* g, path_t* p)
{
  //printf("ddd\n");
  unsigned long long n= 0; //set a value n
  int32_t i; //temperary variable
  int32_t index; // index variable
  int32_t shift; // shift variable
  for(i = 0; i < p->n_vertices; i++ )
  {
    index = (p->id)[i]; //index value of that vertex
  //  printf("before\n");
    shift =(g->vertex)[index].mm_bit; // how many bit show we shift
    //printf("after\n");
    n |= (1ULL << (63 - shift));//shift and oring old value;
  }
  p->minimap = n;//fill minimap
}

//binary search, increasing order
/*first set which element show we start searching(the least index) and then check if Matched
if not change to next element in v2, if mathc change to next v1 and v2*/
int32_t
merge_vertex_sets (const vertex_set_t* v1, const vertex_set_t* v2,
		   vertex_set_t* vint)
{
    int mark;//mark which element we should start searching.
    int j = 0;//initial condition, v1
    int i = 0;//v2
    int k = 0;//temperary variable
    while(i<v2->count)//check if we find all element in v2
      {
        mark = (v1->id)[j];//mark which element we should start searching.
        if(v2->id[i] < mark) //if not match
        {
          i++; //next element
          continue;//next element;
        }
        else //if match
        {
          (vint->id)[k] = mark; //put in set
          k++;
          vint->count = k;//we have find k match item
        }
        j++;//next element in v1
        i++;//next element in v2
        if(j >= v1->count) //if we search all set in v1
        {
          break;
        }
      }
      if(vint->count>0) //if we find more than 1 match
      {
        return 1;
      }
    return 0;
}
