from google.cloud import vision
import io
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'Recipe-Bot-e5867579a186.json'
client = vision.ImageAnnotatorClient()

def tokenizer(recipe_folder_name):
    cwd = os.getcwd()
    recipes_folder = 'Images_recipes'

    # Process image and extract ingredient list and instructions list
    filepath = os.path.join(cwd, recipes_folder, recipe_folder_name)

    all_files = []

    for filename in sorted(os.listdir(filepath)):
        with io.open(os.path.join(filepath, filename), 'rb') as image_file:
            content = image_file.read()
            image = vision.types.Image(content=content)
            response = client.text_detection(image=image)
            text = response.full_text_annotation.text
            text = text.replace('•', '')
            text = text.split('\n')
            all_files.append(text)

    all_text = []
    for list in all_files:
        all_text = all_text + list

    ingredient_index = 0
    instructions_index = 0

    for i in range(len(all_text)):
        if 'ingredients' in all_text[i].lower():
            ingredient_index = i
        if 'instructions' in all_text[i].lower():
            instructions_index = i

    ingredients = all_text[ingredient_index+1:instructions_index]
    instructions = all_text[instructions_index+1:]

    # Read in food_list
    food_list = [line.rstrip('\n').lower() for line in open('food_list.txt')]
    food_list = set(food_list)

    # Process Ingredients
    ingredients_dict = {}

    for item in food_list:
        for ingredient in ingredients:
            if item in ingredient:
                ingredients_dict[item] = ingredient

    # Remove repeating keys/values (olive, oil and olive oil will all generate separate keys in the code above)
    repeat_keys = []
    for key1 in ingredients_dict:
        for key2 in ingredients_dict:
            # avoid deleting identical keys
            if key1 != key2:
                if ingredients_dict[key1] == ingredients_dict[key2]:
                    shorter_key = min(key1, key2, key=len)
                    repeat_keys.append(shorter_key)

    for item in repeat_keys:
        try:
            del ingredients_dict[item]
        except KeyError:
            pass

    # Process Instructions
    for item in instructions:
        if len(item) == 0 or len(item) == 1:
            instructions.remove(item)

    index = -1
    new_instructions = []
    for i in range(len(instructions)):
        if instructions[i][0].isdigit() and instructions[i][1] == '.':
            index = index + 1
            new_instructions.append(instructions[i])
        elif instructions[i][0].isdigit() and instructions[i][2] == '.':
            index = index + 1
            new_instructions.append(instructions[i])
        else:
            new_instructions[index] = new_instructions[index] + instructions[i]

    return ingredients_dict, new_instructions
