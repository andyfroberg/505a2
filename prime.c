// #include <stdio.h>
// #include <stdlib.h>
// #include <unistd.h>  //Header file for sleep(). man 3 sleep for details.
// #include <pthread.h>
  // 
// // A normal C function that is executed as a thread
// // when its name is specified in pthread_create()
// void *thread(void *vargp)
// {
    // sleep(1);
    // printf("Printing GeeksQuiz from Thread \n");
    // return NULL;
// }
   // 
// int main()
// {
    // pthread_t thread_id;
    // printf("Before Thread\n");
    // pthread_create(&thread_id, NULL, thread, NULL);
    // pthread_join(thread_id, NULL);
    // printf("After Thread\n");
    // exit(0);
// }







#include <stdio.h>
#include <pthread.h>

int main() {
	
    int number, i, j;
    printf("The Sieve of Eratosthenes is a method for finding all prime numbers\nup to a given number. Enter a whole number up to which you would like\nthe program to find all the primes: ");
    scanf("%d", &number);

	// Make global array for all threads to write to
    int primes[number+1];

    //populating array with naturals numbers
    for (i = 2; i <= number; i++) {
        primes[i] = i;
	}
	
    i = 2;
    while ((i * i) <= number) {
        if (primes[i] != 0) {
            for (j = 2; j < number; j++) {
                if (primes[i] * j > number) {
                    break;
                } else {
                    // Instead of deleteing , making elemnets 0
                    primes[primes[i]*j] = 0;
                }
            }
        }
        i++;
    }

    for (i = 2; i <= number; i++) {
        //If number is not 0 then it is prime
        if (primes[i] != 0) {
            printf("%d\n", primes[i]);
        }
    }
    
    return 0;
}    
