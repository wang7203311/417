#include <stdint.h>
#include <stdio.h>

#include "mp5.h"
#include "mp9.h"

/*for source find all node in r1 and delete node not in r2, for destination,
find all node in r1 and delete all node not in r2. if there are node, we call djikstra function,
if it return 1, means we can match correctly, if not we return 0*/
int32_t
match_requests (graph_t* g, pyr_tree_t* p, heap_t* h,
		request_t* r1, request_t* r2,
		vertex_set_t* src_vs, vertex_set_t* dst_vs, path_t* path)
{
		//common source
		//find node in r1
		src_vs->count = 0;
		find_nodes(&(r1->from), src_vs, p, 0);

		//delete node not in r2
		trim_nodes(g, src_vs, &(r2->from));
		//check if we have node;
		if(0==(src_vs->count))
		{
			return 0;
		}
		//common destination
		//find node in r1
	 dst_vs->count = 0;
		find_nodes(&(r1->to), dst_vs, p, 0);

		//delete node not in r2
		trim_nodes(g, dst_vs, &(r2->to));
		//check if we have node
		if(0==(dst_vs->count))
		{
			return 0;
		}
		//call dijkstra to find route
		if(1 == dijkstra(g,h,src_vs,dst_vs,path))
		{
			free(path->id);
			free(vs->id);
			return 1; //if dijkstra return 1, we match successfully
		}
		return 0;
}
