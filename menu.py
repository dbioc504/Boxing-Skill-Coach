import shadow_f


def app_menu():
  # start of app_menu variables
  filename = "skills.txt"
  all_skills = {"Boxing": [], "Pressure": [], "Dogwork": []}
  shadow_f.read_from_file(filename, all_skills)
  print("-------------------")
  menu_prompt = "1.)Enter Skill\n2.)Display Skills\n3.)Round Skills\n4.)Exit\n"
  menu_options = [1, 2, 3, 4]
  main_menu_choice = proper_input(menu_prompt, menu_options)
  app_on = True
  while app_on:
    match int(main_menu_choice):
      case 1:
        print("\n")
        enter_skill_page(filename, all_skills)
        break
      case 2:
        print("\n")
        shadow_f.display_skills(all_skills)
        display_prompt = "Press 1 to return to menu\n"
        display_options = [1]
        proper_input(display_prompt, display_options)
        print("\n")
        app_menu()
        break
      case 3:
        print("\n")
        round_skill_page(filename, all_skills)
        break
      case 4:
        app_on = False
  return


def proper_input(prompt, input_list, input_type=str):
  user_input = input(prompt)
  if not user_input.strip():
    print("Please try again.")
    return proper_input(prompt, input_list)
  if isinstance(user_input, str):
    user_input = user_input.upper()
  if isinstance(input_list[0], int):
    user_input = int(user_input)
  # Check if the input is empty or appropriate
  if user_input not in input_list:
    print("Please try again.")
    return proper_input(prompt, input_list)
  return user_input


def enter_skill_page(filename, skill_dict):
  # displaying current skills
  print("Current skills and techniques:")
  shadow_f.display_skills(skill_dict)
  print()
  # actually entering skill
  shadow_f.enter_skill(filename)
  shadow_f.read_from_file(filename, skill_dict)
  # showing the new updated dictionary
  print("\nSkill added. Updated skills and techniques:")
  shadow_f.display_skills(skill_dict)
  print()
  # prompting user for more skill entries
  enter_prompt = "Enter another skill?\n1.)Yes\n2.)No\n"
  enter_options = [1, 2]
  enter_choice = proper_input(enter_prompt, enter_options)
  match int(enter_choice):
    case 1:
      print("\n")
      enter_skill_page(filename, skill_dict)
      shadow_f.read_from_file(filename, skill_dict)
    case 2:
      print("\n")
      app_menu()
  return


def round_skill_page(filename, skill_dict):
  shadow_f.read_from_file(filename, skill_dict)
  prompt = "Specialized or Balanced?\n1.)Specialized\n2.)Balanced\n"
  options = [1, 2]
  choice = proper_input(prompt, options)
  match int(choice):
    case 1:
      shadow_f.specialized_loop(skill_dict)
    case 2:
      shadow_f.skill_loop(skill_dict)
  skill_loop_prompt = "More rounds?\n1.)Yes\n2.)No\n"
  skill_loop_options = [1, 2]
  skill_loop_choice = proper_input(skill_loop_prompt, skill_loop_options)
  match int(skill_loop_choice):
    case 1:
      print("\n")
      round_skill_page(filename, skill_dict)
    case 2:
      print("\n")
      app_menu()
  return
