#include <stdint.h>
#include <stdlib.h>

#include "mp10.h"

/*use malloc to create a new vertex_set_t and check if we fail, if not
intialize count and id*/
vertex_set_t*
new_vertex_set ()
{
    //create a new vertex_t
    vertex_set_t* n_v =(vertex_set_t*)malloc(sizeof(vertex_set_t));
    if(n_v != NULL) //if we success
    {
      n_v->count =0; //initialize count
      n_v->id = NULL; //initialize id
      return n_v; //return pointer
    }
    return NULL;
}

/*check if id is NULL if not, free it first, then free vs*/
void
free_vertex_set (vertex_set_t* vs)
{
  if(vs->id != NULL) //if id is not NULL
  {
    free(vs->id); // free id first
  }
  free(vs); //free vs
}

/*use malloc to create a new path_t and check if we fail, if not
intialize n_vertices and id*/
path_t*
new_path ()
{
  //create a new path_t
  path_t* n_p =(path_t*)malloc(sizeof(path_t));
  if(n_p != NULL) //check if we fail
  {
    n_p->n_vertices =0; //intialize n_vertices
    n_p->id = NULL; //initialize id
    return n_p;// return pointer
  }
  return NULL;
}

/*check if id is NULL if not, free it first, then free path*/
void
free_path (path_t* path)
{
  if(path->id != NULL) //check if id is NULL
  {
  free(path->id);//free id first
  }
  free(path);// free path
}
