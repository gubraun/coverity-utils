#include "mythreads.h"

my_mutex_t _mx;

struct s_memory_t {
    int data;
    int meta;
};

void update_data(s_memory_t *m)
{
    my_mutex_lock(&_mx);
    m->data = 0xdeadbeef;
    if (m->meta != 0) {
	return; // +missing_unlock
    }
    my_mutex_unlock(&_mx);
}

int main()
{
    s_memory_t shrd;

    update_data(&shrd);

    return 0;
}
