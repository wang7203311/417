#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "mp5.h"
#include "mp9.h"

#define MY_INFINITY   1000000000

void
/*check the region one by one, if it is posible that the locale in that region
we do the recursion to check the children. if we find the leaf node, we put in to set
and return.*/
find_nodes (locale_t* loc, vertex_set_t* vs, pyr_tree_t* p, int32_t nnum)
{
    // Do not modify the following line nor add anything above in the function.
    int index;//index variable
    int temp; //temporary variable
    int sort; //sort index
    record_fn_call ();
    //temperary variable
    //the number of node we find;
    if((4*nnum +1) >= p->n_nodes)
    {
      if(1 == in_range(loc, (p-> node)[nnum].x, (p-> node)[nnum].y_left))//check if it is in range
      {
        if(vs->id == NULL) //check if the id is null
        {
           vs->id = (int32_t*)malloc(100*sizeof(int32_t));//malloc 40 byte
        }

        vs->id[vs->count] = (p->node)[nnum].id; //if in range, put it in the set
        (vs->count) ++; //increament the thing we find
      }
      return;
    }
     //check if it is possible that the locale stay in the 4n+1 region
    //  printf("x = %d, yl = %d, yr = %d, range = %d\n", (p-> node)[nnum].x, (p-> node)[nnum].y_left, (p-> node)[nnum].y_right,(loc->range));
     if((p-> node)[nnum].x >= (loc->x) - (loc->range) &&
    (p-> node)[nnum].y_left >= (loc->y) - (loc->range))
    {
      find_nodes(loc, vs, p, 4*nnum+1); //if yes, we do recursion;
    }
    //check if it is possible that the locale stay in the 4n+2 region
    if((p-> node)[nnum].x < (loc->x) + (loc->range) &&
    (p-> node)[nnum].y_right >= (loc->y) - (loc->range))
    {
      find_nodes(loc, vs, p, 4*nnum+2); //if yes, we do recursion;
    }
    //check if it is possible that the locale stay in the 4n+3 region
    if((p-> node)[nnum].x >= (loc->x) - (loc->range) &&
    (p-> node)[nnum].y_left < (loc->y) + (loc->range))
    {
      find_nodes(loc, vs, p, 4*nnum+3);//if yes, we do recursion
    }
    //check if it is possible that the locale stay in the 4n+4 region
    if((p-> node)[nnum].x < (loc->x) + (loc->range) &&
    (p-> node)[nnum].y_right < (loc->y) + (loc->range))
    {
      find_nodes(loc, vs, p, 4*nnum+4); //if yes, we do recursion
    }
    //heapify;
    for(sort = 2; vs->count>=sort; sort ++)
      {
        temp = (vs->id)[sort -1];
          for(index = sort -1; 0 < index; index--)
          {
            if(temp >=(vs->id)[index -1])
            {
              break;
            }
            (vs->id)[index] = (vs->id)[index-1];
          }
          (vs->id)[index] = temp;
      }
}
/*check the index in vertex_set, use in_range function to check if it is in in_range
if not, we pop it out the set*/

void
trim_nodes (graph_t* g, vertex_set_t* vs, locale_t* loc)
{
    int i;  //temperary variable
    int j;  //temperary variable
    int index; //index
    for(i = 0;i< vs->count; i++) //loop end until we check all element
      {
       //printf("%d\n", vs->count );
        // printArray(vs->id, 16);
        index = (vs-> id)[i]; //the index of the vertex
        //if not in range
        if(1 != in_range(loc,(g-> vertex)[index].x,(g-> vertex)[index].y))
          {
            (vs->count)--; //decrement the thing we find
            //left shift the remain element
            for(j = i; j< vs->count; j++)
            {
              vs->id[j] = vs->id[j+1];
            }
          //  printf("%d\n", vs->count);
              vs->id[vs->count] = 0; //set the last element in previous array be 0
              i = i-1;
          }
      }
}
//heap help function
//swap two number in array
static void swap(int * a, int* b){
  int t = *a; //t is what a point to
  *a = *b;  //a point to what b points
  *b = t;   //b point to t
}
//heapify function, rerange in decreasing order
//compare two element with their parents, it it greater than parents, swap two
static void heapify(int* arr, int n, int i,graph_t* g)
{
    int largest = i;  // set root as the largest value
    int l = 2*i + 1;  // left child index
    int r = 2*i + 2;  // right child index
    // If left child is larger than root
    if (l < n && (g->vertex)[arr[l]].from_src > (g->vertex)[arr[largest]].from_src)
        largest = l; // largest value is left child
    // If right child is larger than largest so far
    if (r < n && (g->vertex)[arr[r]].from_src > (g->vertex)[arr[largest]].from_src)
        largest = r; //largest value is right child
    // If largest is not root
    if (largest != i)
    {
        swap(&arr[i], &arr[largest]); //swap the two distance value in heap
        // Recursively heapify the affected sub-tree
        heapify(arr, n, largest, g);
    }
}
//make a min heap
static void minheap(int* arr, int n, graph_t* g)
{
    // build heap
    int i; //current node
    for (i = n/2 - 1; i >= 0; i--)
        {
          heapify(arr, n, i, g);
        }
    // One by one extract an element from heap
    for (i=n-1; i>=0; i--)
    {
        // Move current root to end
        swap(&arr[0], &arr[i]); //swap two distance from heap
        // call heapify function
        heapify(arr, i, 0, g);
    }
}
/*first set all distance in source locale as 0, check their neighbor and put distance
in to heap and make a min heap. pop the smallest element and check next vertex until we find_nodes
next is our destination. put it in path and use their predecessor to fill the array, if reach
MAX_PATH_LENGTH, return 0*/

int32_t
dijkstra (graph_t* g, heap_t* h, vertex_set_t* src, vertex_set_t* dest,
          path_t* path)
{
    int i; //temperary variable, use for loop
    int j; //temperary variable, use for loop
    int k; //temperary variable, use for loop
    int l;
    int index; //index variable
    int new_distance; //new_distance variable
    int old_distance; //old distance variable
    int nei_id; //neighbor's index
    int child;
    int parent;
    for(i = 0; i<(g->n_vertices); i++)
    {
      (g->vertex)[i].from_src = MY_INFINITY; //all distance is infinity
    }
    //find the starting point
    for(i = 0; i<src->count;i++)
    {
      index = src->id[i];  //the index of vertex in source locale
      (g->vertex)[index].from_src = 0; //new distance
      // (h->elt)[i]= (g->vertex)[index].from_src; //put the distance in to heap
      // h_id[i]  = src->id[i];//put id into h_id
      (g->vertex)[index].pred = MY_INFINITY; //set start point no predecessor.
    }
    for(i = 0; i< g->n_vertices; i++) //pass pointer to heap and corresponding distance to array
    {
      (h->elt)[i] = i; //put index heap
      //printf("dis = %d\n", (h->elt)[i]);
    }
    h->n_elts = g->n_vertices;
    //heapify distance and swap
    minheap(h->elt, h->n_elts, g);
    index = (h->elt)[0]; //current node's id

    // h->n_elts = src->count; //things in heap equal to things in source locale
    //if the id is MY_INFINITY or I find the destination, we end search
    while(h->n_elts != 0 && (g->vertex)[index].from_src != MY_INFINITY)
    {
      //printf("dis = %d", (h->elt)[0]);
    //check the neighbors, if finished that node mark infinity -1
    //put the neiborhood in array
    for(j = 0; j<(g->vertex)[index].n_neighbors;j++)
    {
      index = (h->elt)[0];
      //define the neighbors new distance= value of predecessor + distance
       new_distance = (g->vertex)[index].from_src + (g->vertex)[index].distance[j];
       //compare the newly calculated distance to current value
       nei_id = (g->vertex)[index].neighbor[j];
      // printf("nei =   %d\n", nei_id ); //define neighbor's index
       old_distance = (g->vertex)[nei_id].from_src; // the previous distance value
       //if the old distance greater  than new distance
       if( old_distance> new_distance)
        {
          (g->vertex)[nei_id].from_src = new_distance; //set new distance be the distance from source
          //change the predecessor
          (g->vertex)[nei_id].pred = index;
        }
    }
    //create a min-heap
    minheap(h->elt, h->n_elts, g);
    // (g->vertex)[index].heap_id = MY_INFINITY -1;//mark the current node as visited;
 //pop the first element and reheapify
    h->n_elts = h->n_elts -1;
    h->elt[0] = h->elt[h->n_elts];
  //reheapify
    minheap(h->elt, h->n_elts, g);
  //  printArray(h->elt, h->n_elts);
    //check if it is in destination
    // printf("ooooo\n");
    for(k=0; k< dest->count; k++)
    {
      if((h->elt)[0]== dest->id[k]) //check if next is destination
      {
        (path->n_vertices) =0; //no thing on path
        path->tot_dist = (g->vertex)[(h->elt)[0]].from_src; //put total distance
        child = (h->elt)[0]; //destination's index
        // parent = (g->vertex)[child].pred;   //define predecessor's index
        path->n_vertices ++; //increament the things on path
        //calculate how many byte we need;
        parent = (g->vertex)[child].pred;
        while(parent != MY_INFINITY)
        {
          parent = (g->vertex)[child].pred;
          child = parent;
          (path->n_vertices)++; //increament things on path
        }
        // (path->n_vertices)++; //how many vertex we find;
        path->id = (int32_t*)malloc((path->n_vertices)*sizeof(int32_t));//malloc
        {
          if(path-> id == NULL)//if we fail
          {
            return 0;//return 0
          }
        }
        path->id[0] = (h->elt)[0]; //put element in  path
        // path->id[(path->n_vertices)] = parent; //put his predecessor's index on path
        child = (h->elt)[0];//initialize child
        for(l = 1; l<(path->n_vertices); l++)
        {
         parent = (g->vertex)[child].pred;   //define predecessor's index
         path->id[l] = parent; //put his predecessor's index on path
         child = parent;//upate child
        }
        return 1;
     }
   }
 }
return 0; //return fail because we check all point
}
