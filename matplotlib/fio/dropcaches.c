#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(int argc, char **argv)
{
    int fd;
    char buf[16];
    ssize_t written;
    int val;

    if(geteuid() != 0){
        fprintf(stderr, "ERROR : not root\n");
        exit(EXIT_FAILURE);
    }

    if(argc != 2){
        fprintf(stderr, "Usage %s <INT>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    val = atoi(argv[1]);
    sprintf(buf, "%d\n", val);

    sync();
    sync();
    sync();

    fd = open("/proc/sys/vm/drop_caches", O_WRONLY | O_CREAT);
    if(fd == -1){
        perror("open");
        exit(EXIT_FAILURE);
    }

    written = write(fd, buf, strlen(buf));
    if(written == -1){
        perror("write");
        exit(EXIT_FAILURE);
    }

    close(fd);
    return 0;
}

