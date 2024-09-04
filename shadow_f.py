import os
import random
import menu


# only for the enter skill don't worry about order
def create_or_write_file(custom_filename, content):
  # Check if the file exists
  if not os.path.exists(custom_filename):
    # Use 'w' mode to create the file if it doesn't exist and write the content
    with open(custom_filename, 'w') as file:
      file.write(content)
  else:
    # Use 'a' mode to append content if the file exists
    with open(custom_filename, 'a') as file:
      file.write(content)
  return


# 2nd function call
def read_from_file(custom_filename, skill_dict):
  # Check if the file exists
  if os.path.exists(custom_filename):
    # Use 'r' mode to read the file
    with open(custom_filename, 'r') as file:
      for line in file:
        line = line.strip()
        # index for collecting technique from line cutting at :
        colon = line.find(":")
        skill = line[0]
        match skill:
          case "B":
            technique = line[colon + 1:]
            if technique not in skill_dict.get("Boxing"):
              skill_dict["Boxing"].append(technique)
          case "P":
            technique = line[colon + 1:]
            if technique not in skill_dict.get("Pressure"):
              skill_dict["Pressure"].append(technique)
          case "D":
            technique = line[colon + 1:]
            if technique not in skill_dict.get("Dogwork"):
              skill_dict["Dogwork"].append(technique)

# end of function
  return


# 1st function call
def enter_skill(filename):
  # asking user for skill pillar
  """
  skill = input(
      "Enter your skill\n(P: Pressure, D:Dogfighting, B: Boxing,\tC: Cancel):\n"
  )
  while skill.upper() not in ['P', 'D', 'B']:
    skill = input(
        "Enter your skill\n(P for Pressure, D for Dogfighting, or B for Boxing):\n"
    )
  """
  skill_prompt = "Enter your skill\n(P:Pressure, D:Dogfighting, B: Boxing,\tC:Cancel):\n"
  skill_options = ['P', 'D', 'B', 'C']
  skill = menu.proper_input(skill_prompt, skill_options)
  if isinstance(skill, str):
    if skill.upper() == 'C':
      return
    else:
      # asking user for specific technique
      technique = input("Enter your technique: ")
      # concatenating string and entering it into file
      content = f"{skill.upper()}:{technique}\n"
      create_or_write_file(filename, content)
    
      return


# actual round loop
def skill_loop(skill_dict):
  # number of rounds
  num = int(input("Rounds: "))
  temp = 1
  curr_round = skill_select(random.choice(list(skill_dict.keys())), skill_dict)
  # create a count for reach time a skill is used
  count_boxing = 0
  count_pressure = 0
  count_dogwork = 0
  # create a used dictionary
  used_skills = {"Pressure": [], "Boxing": [], "Dogwork": []}
  # round loop
  while temp <= num:
    curr_skill = curr_round[0]
    curr_tech = curr_round[1]
    print(f"Round {temp}:\n{curr_skill}:\t{curr_tech}\n")
    # storing used skills/techniques
    used_update_value = used_skills.get(curr_skill)
    if used_update_value is not None:
      used_update_value.extend(curr_tech)
    else:
      used_update_value = curr_tech
    used_skills.update({curr_skill: used_update_value})
    # removing techniques from current skill
    tech_value = skill_dict.get(curr_skill)
    skill_dict.update(
        {curr_skill: [x for x in tech_value if x not in curr_tech]})
    # incrementing count for each skill
    match curr_skill:
      case "Boxing":
        count_boxing += 1
      case "Pressure":
        count_pressure += 1
      case "Dogwork":
        count_dogwork += 1
    # collecting the skill with the min of all counts
    all_counts = [count_boxing, count_pressure, count_dogwork]
    min_count = min(all_counts)
    min_indices = [
        i for i, count in enumerate(all_counts) if count == min_count
    ]
    skill_index = random.choice(min_indices)
    new_skill = ""
    match skill_index:
      case 0:
        new_skill = "Boxing"
      case 1:
        new_skill = "Pressure"
      case 2:
        new_skill = "Dogwork"

    # refilling list if empty
    if len(skill_dict.get(new_skill)) < 1:
      skill_dict.update({new_skill: used_skills.get(new_skill)})
      used_skills.update({new_skill: []})
    # selecting new techniques
    next_round_techs = skill_select(new_skill, skill_dict)
    curr_round = next_round_techs
    # iterating to the next round
    temp += 1
    # end of function
  return


# only used skill_loop don't worry about order
def skill_select(skill, skill_dict):
  techs = ""
  if len(skill_dict.get(skill)) > 1:
    techs = random.sample(skill_dict.get(skill), 2)
  else:
    techs = skill_dict[skill]
  return skill, techs


# show skills
def display_skills(skill_dict):
  for skill in list(skill_dict.keys()):
    print(f"{skill}:\t{skill_dict.get(skill)}")
  return



# more of an algorithm
def specialized_loop(skill_dict):
  # ask user to select area of focus
  focus_skill_prompt = "Select the category you want to focus on:\n" \
  "P) Pressure\tB) Boxing\tD) Dogfighting\tC) Cancel\t"
  focus_skill_list = ["P","B","D","C"]
  focus_skill_entry = menu.proper_input(focus_skill_prompt,focus_skill_list)
  focus_skill = ""
  match focus_skill_entry:
    case "P":
      focus_skill = "Pressure"
    case "B":
      focus_skill = "Boxing"
    case "D":
      focus_skill = "Dogwork"
    case "C":
      menu.app_menu()
      return
  # ask user how many number of rounds
  round_no_prompt = "Rounds: "
  round_no = menu.proper_input(round_no_prompt, list(range(-50,50)), input_type=int)
  # TODO calculate how many times the skill will be distributed
  focused_rounds = int(round_no * 0.7)
  other_rounds = round_no - focused_rounds
  # TODO incoporate an algorithm to randomize the skills but make sure \
  round_choices = [focus_skill] * focused_rounds
  other_skills = [skill for skill in list(skill_dict.keys()) if skill != focus_skill]
  round_choices += random.choices(other_skills,k=other_rounds)
  # for the focus skill takes up 70% of the rounds
  random.shuffle(round_choices)
  used_skills = {"Pressure": [], "Boxing": [], "Dogwork": []}
  temp_round = 1
  # skill loop
  for skill in round_choices:
    # skill select
    curr_round = skill_select(skill,skill_dict)
    curr_skill = curr_round[0]
    curr_tech = curr_round[1]
    print(f"Round {temp_round}:\n{curr_skill}:\t{curr_tech}\n")
    temp_round += 1
    # storing used techniques in used_skills
    used_update_value = used_skills.get(curr_skill)
    used_update_value.extend(curr_tech)
    used_skills.update({curr_skill:used_update_value})
    # removing current skills from skill dictionary
    tech_value = skill_dict.get(curr_skill)
    skill_dict.update({curr_skill:[x for x in tech_value if x not in curr_tech]})
    # refilling list if empty
    if len(skill_dict.get(curr_skill)) < 1:
      skill_dict.update({curr_skill:used_skills.get(curr_skill)})
      used_skills.update({curr_skill:[]})
  return