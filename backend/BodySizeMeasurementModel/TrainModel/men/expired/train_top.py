from menchart import men_size_charts

def get_user_input():
    chest = float(input("Enter your chest measurement in cm: "))
    waist = float(input("Enter your waist measurement in cm: "))
    arm_length = float(input("Enter your arm length measurement in cm: "))
    neckline = float(input("Enter your neckline measurement in cm: "))
    style = input("Enter the shirt style (regular/long): ").strip().lower()
    clothing_type = input("Enter the clothing type (tshirt, shirt, sweatshirt, hoodie, jacket): ").strip().lower()
    return {'chest_cm': chest, 'waist_cm': waist, 'arm_length_cm': arm_length, 'neckline_cm': neckline, 'style': style, 'clothing_type': clothing_type}

def find_best_fit(user_measurements, size_chart):
    best_fit = None
    min_diff = float('inf')
    
    for size, size_data in size_chart.items():
        chest_range = size_data['chest_cm']
        waist_range = size_data['waist_cm']
        arm_length = size_data['arm_length_cm']
        neckline = size_data['neckline_cm']
        
        diff = 0
        if isinstance(chest_range, tuple):
            diff += max(0, abs(user_measurements['chest_cm'] - chest_range[0]), abs(user_measurements['chest_cm'] - chest_range[1]))
        else:
            diff += abs(user_measurements['chest_cm'] - chest_range)
        
        if isinstance(waist_range, tuple):
            diff += max(0, abs(user_measurements['waist_cm'] - waist_range[0]), abs(user_measurements['waist_cm'] - waist_range[1]))
        else:
            diff += abs(user_measurements['waist_cm'] - waist_range)
        
        if isinstance(arm_length, tuple):
            diff += max(0, abs(user_measurements['arm_length_cm'] - arm_length[0]), abs(user_measurements['arm_length_cm'] - arm_length[1]))
        else:
            diff += abs(user_measurements['arm_length_cm'] - arm_length)
        
        if isinstance(neckline, tuple):
            diff += max(0, abs(user_measurements['neckline_cm'] - neckline[0]), abs(user_measurements['neckline_cm'] - neckline[1]))
        else:
            diff += abs(user_measurements['neckline_cm'] - neckline)
        
        if diff < min_diff:
            min_diff = diff
            best_fit = size
    
    return best_fit

def get_size_chart(clothing_type, style):
    if clothing_type == 'tshirt' or clothing_type == 'tops':
        return men_size_charts['tops_tshirts'][style]
    elif clothing_type == 'shirt':
        return men_size_charts['shirts'][style]
    elif clothing_type == 'sweatshirt' or clothing_type == 'hoodie':
        return men_size_charts['sweatshirts_hoodies'][style]
    elif clothing_type == 'jacket' or clothing_type == 'coats':
        return men_size_charts['jackets_coats'][style]
    elif clothing_type == 'shorts':
        return men_size_charts['shorts'][style]
    else:
        print("Invalid clothing type input. Please enter a valid clothing type.")
        exit()

if __name__ == "__main__":
    user_measurements = get_user_input()
    
    style = user_measurements['style']
    clothing_type = user_measurements['clothing_type']
    
    size_chart = get_size_chart(clothing_type, style)
    
    best_size = find_best_fit(user_measurements, size_chart)
    
    print(f"The best size for you for {clothing_type} is: {best_size}")
