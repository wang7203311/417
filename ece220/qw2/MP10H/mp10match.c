#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "mp5.h"
#include "mp10.h"


//
// These variables hold the heads of two singly-linked lists of
// requests.
//
// The avaialble list consists of unpaired requests: partner
// should be NULL, and next is used to form the list.
//
// The shared list consists of groups with non-empty start and end
// vertex intersections.  Only one of the requests in the group is in
// the list.  The others are linked through the first's partner field
// and then through the next field of the others in the group.  The
// next field of the first request in a group is used to form the
// shared list.
//
// Note: for MP2, you should only build groups of two in the shared
// list.
//

static request_t* available = NULL;
static request_t* shared = NULL;

static void
free_request (request_t* r)
{
    free_vertex_set (r->src_vs);
    free_vertex_set (r->dst_vs);
    if (NULL != r->path) {
	free_path (r->path);
    }
    free (r);
}


static void free_alloc(request_t* avaialable, request_t* shared)
{
  request_t** temp;
  //free avaialble
  for(temp = &available; *temp != NULL; temp = &((*temp)->next))
    {
      free_request(*temp);
    }
  //free share
  for(temp = &shared; *temp != NULL; temp = &((*temp)->next))
    {
      //free partner first
      free_request((*temp)->partner);
      free_request(*temp);
    }
}

int32_t
handle_request (graph_t* g, pyr_tree_t* p, heap_t* h, request_t* r)
{
  request_t** search;
  request_t** temp;
  uint64_t compare_src;
  uint64_t compare_dst;
  int32_t size;
  //if it is the first request
  if(available == NULL)
  {
    r->src_vs = new_vertex_set();
    if(r->src_vs== NULL)
        {return 0;}
    find_nodes(&(r->from),r->src_vs, p, 0);
    build_vertex_set_minimap(g, r->src_vs);
    r->dst_vs = new_vertex_set();
    if(r->dst_vs == NULL)
        {
          return 0;
        }
    find_nodes(&(r->to), r->dst_vs, p, 0);
    build_vertex_set_minimap(g, r->dst_vs);
    r->partner = NULL;
    r->path = NULL;
    r->next = NULL;

    available = r;
    return 1;
  }
  //if it is not first request;
  else
    {
    //Allocate vertex_set and new_path
    //fill in vertex_set
    r->src_vs = new_vertex_set();
    if(r->src_vs== NULL)
        {
          free_alloc(available, shared);
          return 0;
        }
    find_nodes(&(r->from), r->src_vs, p, 0);
    build_vertex_set_minimap(g, r->src_vs);
    r->dst_vs = new_vertex_set();
    if(r->dst_vs== NULL)
        {
          free_alloc(available, shared);
          return 0;
        }
    find_nodes(&(r->to), r->dst_vs, p, 0);
    // printf("%lu\n", compare_dst);
    build_vertex_set_minimap(g, r->dst_vs);
    //check for match
    //searching
    for(search = &available; *search != NULL; search = &((*search)->next))
      //check src and dst
    {
      //compare minimap;
      compare_src = (*search)->src_vs->minimap  & r->src_vs-> minimap;
      compare_dst = (*search)->dst_vs->minimap  & r->dst_vs-> minimap;
      if(compare_src!= 0 && compare_dst != 0)
      {
        //used for src
        vertex_set_t* vint_src = new_vertex_set();
        if(vint_src == NULL)
        {
          free_alloc(available, shared);
        }
        if((*search)->src_vs->id_array_size > r->src_vs->id_array_size)
        {
          size = (*search)->src_vs->id_array_size;
        }
        else
        {
          size = r->src_vs->id_array_size;
        }
        vint_src->id =(int32_t*)malloc(size*sizeof(int32_t));
        if(vint_src->id == NULL)
        {
          free_vertex_set(vint_src);
          free_alloc(available, shared);
        }
        //for dst
        vertex_set_t* vint_dst = new_vertex_set();
        if(vint_dst == NULL)
        {
          free_alloc(available, shared);
        }
        if((*search)->dst_vs->id_array_size > r->dst_vs->id_array_size)
        {
          size = (*search)->dst_vs->id_array_size;
        }
        else
        {
          size = r->dst_vs->id_array_size;
        }
        vint_dst->id =(int32_t*)malloc(size*sizeof(int32_t));
        if(vint_dst->id == NULL)
        {
          free_vertex_set(vint_dst);
          free_alloc(available, shared);
        }
        //merge
        if(1 == merge_vertex_sets((*search)->dst_vs,r->dst_vs, vint_dst) &&
        1 == merge_vertex_sets((*search)->src_vs,r->src_vs, vint_src))
          {
              // deep search path
              // call dijkstra check path
              path_t* path_d= new_path();
              if(path_d == NULL)
                {
                  free_alloc(available, shared);
                  return 0;
                }
                printf("lllll\n");
              if(1 == dijkstra(g, h, vint_src, vint_dst, path_d))
              {
                //add to share list
                  build_path_minimap(g, path_d);
                  if(shared == NULL)
                    {
                      shared = r;
                    }
                  else
                    {
                      for(temp = &shared; *temp != NULL; temp = &((*temp)->next))
                          {
                          }
                        temp = &r;
                    }
                  //set partner and path and next;
                  r->partner = *search;
                  r->path = path_d;
                  r->src_vs = vint_src;
                  r->dst_vs = vint_dst;
                  r->next = NULL;
                  (*search)->src_vs = vint_src;
                  (*search)->dst_vs = vint_dst;
                  (*search)->path = path_d;
                  (*search)->next = NULL;
                  //remove from available;
                  search = &((*search)->next);
              }
            else
            {
              free_path(path_d);
            }
        }
        free_vertex_set(vint_dst);
        free_vertex_set(vint_src);
      }
    }
    //if we not find match, add to avalilable list
    search = &r;
    r->partner = NULL;
    r->path = NULL;
    r->next = NULL;
    return 1;
  }
  return 0;
}


void
print_results ()
{
    request_t* r;
    request_t* prt;

    printf ("Matched requests:\n");
    for (r = shared; NULL != r; r = r->next) {
        printf ("%5d", r->uid);
	for (prt = r->partner; NULL != prt; prt = prt->next) {
	    printf (" %5d", prt->uid);
	}
	printf (" src=%016lX dst=%016lX path=%016lX\n", r->src_vs->minimap,
		r->dst_vs->minimap, r->path->minimap);
    }

    printf ("\nUnmatched requests:\n");
    for (r = available; NULL != r; r = r->next) {
        printf ("%5d src=%016lX dst=%016lX\n", r->uid, r->src_vs->minimap,
		r->dst_vs->minimap);
    }
}


int32_t
show_results_for (graph_t* g, int32_t which)
{
    request_t* r;
    request_t* prt;

    // Can only illustrate one partner.
    for (r = shared; NULL != r; r = r->next) {
	if (which == r->uid) {
	    return show_find_results (g, r, r->partner);
	}
	for (prt = r->partner; NULL != prt; prt = prt->next) {
	    if (which == prt->uid) {
		return show_find_results (g, prt, r);
	    }
	}
    }

    for (r = available; NULL != r; r = r->next) {
        if (which == r->uid) {
	    return show_find_results (g, r, r);
	}
    }
    return 0;
}

void
free_all_data ()
{
    request_t* r;
    request_t* prt;
    request_t* next;

    // All requests in a group share source and destination vertex sets
    // as well as a path, so we need free those elements only once.
    for (r = shared; NULL != r; r = next) {
	for (prt = r->partner; NULL != prt; prt = next) {
	    next = prt->next;
	    free (prt);
	}
	next = r->next;
	free_request (r);
    }

    for (r = available; NULL != r; r = next) {
	next = r->next;
	free_request (r);
    }
}
