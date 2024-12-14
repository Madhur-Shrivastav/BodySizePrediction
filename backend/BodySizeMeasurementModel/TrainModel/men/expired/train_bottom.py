from menchart import men_size_charts,men_size_charts_2

def get_user_input():
    clothing_type = input("Enter the clothing type (tshirt, shirt, sweatshirt, hoodie, jacket, jeans, trousers, shoes): ").strip().lower()

    # Handle both singular and plural inputs for jeans/trousers
    if clothing_type == 'jeans' or clothing_type == 'trousers':
        waist = float(input("Enter your waist measurement in cm: "))
        low_hip = float(input("Enter your low hip measurement in cm: "))
        inseam_length = float(input("Enter the inseam length (30, 32, 34) in inches: "))
        return {'waist_cm': waist, 'low_hip_cm': low_hip, 'inseam_length': inseam_length, 'clothing_type': clothing_type}
    
    elif clothing_type == 'shoes':
        foot_length = float(input("Enter your foot length in cm: "))
        return {'foot_length_cm': foot_length, 'clothing_type': clothing_type}

    else:
        chest = float(input("Enter your chest measurement in cm: "))
        waist = float(input("Enter your waist measurement in cm: "))
        arm_length = float(input("Enter your arm length measurement in cm: "))
        neckline = float(input("Enter your neckline measurement in cm: "))
        style = input("Enter the shirt style (regular/long): ").strip().lower()
        return {'chest_cm': chest, 'waist_cm': waist, 'arm_length_cm': arm_length, 'neckline_cm': neckline, 'style': style, 'clothing_type': clothing_type}

def find_best_fit(user_measurements, size_chart):
    best_fit = None
    min_diff = float('inf')
    
    for size, size_data in size_chart.items():
        diff = 0
        if user_measurements['clothing_type'] == 'jeans' or user_measurements['clothing_type'] == 'trousers':
            waist_range = size_data['waist_cm']
            low_hip_range = size_data['low_hip_cm']
            length_range = size_data[f"{user_measurements['inseam_length']}inch_length_cm"]
            
            if isinstance(waist_range, tuple):
                diff += max(0, abs(user_measurements['waist_cm'] - waist_range[0]), abs(user_measurements['waist_cm'] - waist_range[1]))
            else:
                diff += abs(user_measurements['waist_cm'] - waist_range)
            
            if isinstance(low_hip_range, tuple):
                diff += max(0, abs(user_measurements['low_hip_cm'] - low_hip_range[0]), abs(user_measurements['low_hip_cm'] - low_hip_range[1]))
            else:
                diff += abs(user_measurements['low_hip_cm'] - low_hip_range)
            
            if isinstance(length_range, tuple):
                diff += max(0, abs(user_measurements['inseam_length'] - length_range[0]), abs(user_measurements['inseam_length'] - length_range[1]))
            else:
                diff += abs(user_measurements['inseam_length'] - length_range)
        
        elif user_measurements['clothing_type'] == 'shoes':
            foot_length = size_data['foot_length_cm']
            diff += abs(user_measurements['foot_length_cm'] - foot_length)
        
        else:
            chest_range = size_data['chest_cm']
            waist_range = size_data['waist_cm']
            arm_length = size_data['arm_length_cm']
            neckline = size_data['neckline_cm']
            
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

def get_size_chart(clothing_type):
    if clothing_type == 'tshirt':
        return men_size_charts['tops_tshirts']
    elif clothing_type == 'shirt':
        return men_size_charts['shirts']
    elif clothing_type == 'sweatshirt':
        return men_size_charts['sweatshirts']
    elif clothing_type == 'hoodie':
        return men_size_charts['hoodies']
    elif clothing_type == 'jacket':
        return men_size_charts['jackets']
    elif clothing_type == 'jeans' or clothing_type == 'trousers':
        return men_size_charts_2['jeans_trousers']
    elif clothing_type == 'shoes':
        return men_size_charts_2['shoes']
    else:
        print("Invalid clothing type input. Please enter a valid clothing type.")
        exit()

if __name__ == "__main__":
    user_measurements = get_user_input()
    
    clothing_type = user_measurements['clothing_type']
    size_chart = get_size_chart(clothing_type)
    
    best_size = find_best_fit(user_measurements, size_chart)
    
    print(f"The best size for you for {clothing_type} is: {best_size}")
