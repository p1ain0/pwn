void eval(int *pool, char sym)
{

  if ( sym == '+' )
  {
    pool[*pool - 1] += pool[*pool];
  }
  else if ( sym > '+' )
  {
    if ( sym == '-' )
    {
      pool[*pool - 1] -= pool[*pool];
    }
    else if ( sym == '/' )
    {
      pool[*pool - 1] /= pool[*pool];
    }
  }
  else if ( sym == '*' )
  {
    pool[*pool - 1] *= pool[*pool];
  }
  --*pool;

}

int parse_expr(char *s, int *pool)
{
    int *pool_tmp = pool;
    char c[0x64] = {0};
    char* num = s;
    int x = 0;
    for(int i = 0; s[i] != 0; i++)
    {
        if(s[i] - '0' > 9)
        {
            int x = &s[i] - num;
            char *s1 = malloc(x + 1);
            memcpy(s1,num,x+1);
            s1[x] = 0;
            if(strcmp(s1,"0") == 0)
            {
                puts("prevent division by zero");
                flush(stdout);
                return 0;
            }
            else
            {
                int num1 = atoi(s1);
                if(num1 > 0)
                {
                    pool[(*pool)++ + 1] = num1;
                    
                }

                if (s[i] == 0 || s[i] - '0' <= 9)
                {
                    num = &s[i + 1];
                    if (c[x] == 0)
                    {
                        c[x] = s[i];
                    }
                    else
                    {
                        switch (s[i])
                        {
                        case '%':
                        case '*':
                        case '/':
                            if (c[x] == '+' || c[x] == '-')
                            {
                                x += 1;
                                c[x] = s[i];
                            }

                            eval(pool, c[x]);
                            c[x] = s[i];
                            break;
                        case '+':
                        case '-':
                            eval(pool, c[x]);
                            c[++x] = s[i];
                            break;
                        default:
                            eval(pool, c[x]);
                            x--;
                        }
                        
                        else
                        {
                            while (x > 0)
                            {
                                eval(pool, c[x]);
                                x--;
                            }
                            else
                            {
                                return 1;
                            }
                        }
                    }
                }
                else
                {
                    puts("expression error!");
                    fflush(stdout);
                    return 0;
                }
            }

        }
    }
}

void calc()
{
    char s[0x400];
    int pool[0x65]; 0x5a0 - 0x40c
    
    while(true)
    {
        bzero(s, sizeof(s));
        int state = get_expr(s, sizeof(s));
        if(state == 0)
            break;
        init_pool(pool);
        state = parse_expr(pool, s);
        if(state != 0)
        {
            //int *result = pool;
            printf("%d\n",pool[pool[0]]);
            flush(stdout);
        }
    }

}


int main(int argc, const char **argv, const char **envp)
{
  ssignal(14, timeout);
  alarm(60);
  puts("=== Welcome to SECPROG calculator ===");
  fflush(stdout);
  calc();
  return puts("Merry Christmas!");
}