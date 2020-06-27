
int a = (100/30);
int b = 100*(100*100);
int c = 100 * 100;

char str_1 = "hello 1";


int main(float _input1, int _input2){

    char str_2 = "hello 2";
    float input1 = _input1;
    int input2 = _input2;
    

    if(a > b){
        a = 30;

        while(a > b){
            a = a / 2;
        }
    }
    else{
        a = a/3;
    }

    for(i = 0 ; (i+3) < 30; i = i + 1){
        for(j = 0; j <10; j = j + 1){
            k = 10;
            while(k > 1){
                a = a + i*j/k;
                k = k - 1;
            }
        }
    }

    return (a*a-a);
}