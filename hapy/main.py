from .exector import run, run2
from .transpiler import transpile
import math

def do(code: str):
   run2(transpile(code))

if __name__ == "__main__":
   # Just testing das'all...
#    code = """
#          import something;

#          # I'm not sure if 'someting.Person' will work...
#          Person = something.Person;

#          class Man inherits Person {
#           has name;
#           has has_pp;
#           has age;
#           has title = 'Mr.';
#           has gender = 'male';

#           use Person(name);

#           def __startwith__() {
#               print("Man was created!")
#           };

#          };

#          frank = Man(name="Frank Abgna", has_pp=True, age=20);

#          print(frank.say_hello());
#          print(issubclass(Man, Person));

#             hello(age=20.3, year=1999);
#             dict = {1:2};
#             print(dict);
#          """

    code = """
        age = 10;

        in (age > 20) {
            nuna("Age is greater!");
        } imbahakaba {
            nuna("Age is less!");
        };
    """

    run2(transpile(code))
