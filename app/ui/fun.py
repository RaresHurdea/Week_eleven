import random


def get_random_fact() -> str:
    facts = [
        "Penguins are flightless birds that have adapted to life in the water.",
        "Emperor penguins can dive to depths of over 500 meters.",
        "Penguins spend up to 75% of their lives in the water.",
        "There are 18 species of penguins in the world."
    ]
    return random.choice(facts)


def draw_ascii_penguin():
    penguin = """

               _~_    
              (o o)   
             /  V  \\  
            /(  _  )\\ 
              ^^ ^^   

         Hello from Antarctica! 
    """
    print(penguin)