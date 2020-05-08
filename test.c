int hello(char chMark, int iNum);   

int main(){
  int a, b, c, aa;
  float abc123, abc_123, abc__;
  bool is_true, is_false;
  char _str;

  a = 0;
  b = 1;
  c = 123;
  aa = -1234

  _str = "My student id is 12345678";
  is_true = true;
  is_false = false;

  abc123 = 0.0;
  abc_123 = 123.000001;
  abc__ = -1235.1223155;

  if (is_true  == ture){
    a = a + 1;
    abc123 = 21.5 * 3.2;
    c = 234 / 22;
    aa = 123 - 123;
  }
  else{
    a = a + -1;
  }

  while(is_false){
    a = a << 1;
    a = a >> 1;
    a = a & a;
    a = a | a;
  }

  for( int i = 0 ; i < 5; i++){
    if( i == 1){
      a = a
    }
    if( i != 1){
      abc123 = -0.123123
    }
    if( i > 1){
      abc123 = -1109.123123
    }
    if( i < 1){
      abc__ = -1234563798.0
    }
    if( i >= 1){
      a = 5 - -6
    }
    if( i <= 1){
      abc__ = 5.2 - -12.0
    }
  }

  hello(_str, a);
  return 0;
}


int hello(char chMark, int iNum)  
{
   return iNum;
}