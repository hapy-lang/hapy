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

#           def when_created() {
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
            printo("Age is greater!");
        } imbahakaba {
            printo("Age is less!");
        };
    """

    code_eng = """
        #! lang=eng
        class Man {
            has name;

            def when_created() {
                print("Hello! Man created");
            };

            def when_printed() {
                return ("My name is " + self.name);
            };
        };

        usman = Man(name="Usman Ahmad");

        print(usman);
    """

    run2(transpile(code))
