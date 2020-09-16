#include <pthread.h>

struct s_memory_t {
    int data;
    int meta;
};

pthread_mutex_t mx;

void update_data(s_memory_t *m)
{
    pthread_mutex_lock(&mx);
    m->data = 0xdeadbeef;
    if (m->meta != 0) {
	return;
    }
    pthread_mutex_unlock(&mx);
}

int main()
{
    s_memory_t shrd;

    update_data(&shrd);

    return 0;
}
