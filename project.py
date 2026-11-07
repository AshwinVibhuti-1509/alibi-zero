import json
import random
import sys


def main():
    with open("data/cases.json", "r") as file:
        data = json.load(file)

    option_menu(data)


def option_menu(data):
    total_score = 0
    while True:
        print("""\n
            1. Start Investigation
            2. How to Play
            3. Exit
            \n"""
        )

        option = input("Enter an option: \n(1, 2, 3)\n >>> ").strip()

        if option == "1":
            while True:
                print(data["case_id"])
                print(data["title"])
                print(data["description"])

                case = generate_case(data)
                earned_points = investigation_menu(case)

                if earned_points is not None:
                    total_score += earned_points
                    print("Investigation complete! ")
                    print(f"Points Earned: {earned_points}")
                    print(f"Total Score: {total_score}")

                else:
                    print("Investigation abadoned! ")
                    print(f"Total Score: {total_score}")


                print("INVESTIGATION ENDED! ")
                while True:
                    print("""\n
                            What would you like to do?

                            1. Play Again
                            2. Return to Main Menu
                            \n"""
                          )

                    replay_choice = input("Enter an option: \n(1, 2)\n >>> ").strip()
                    if replay_choice in ("1", "2"):
                        break

                    print("Invalid option! Please enter 1 or 2.")

                if replay_choice == "1":
                    continue

                elif replay_choice == "2":
                    break

        elif option == "2":
            print("""
        ======================== HOW TO PLAY =========================

        Welcome to ALIBI ZERO!

        A valuable diamond has disappeared from the Grand Museum.
        Four suspects have provided statements about their movements,
        but exactly one suspect has an inconsistent alibi.

        YOUR OBJECTIVE:
        Identify the suspect whose claimed journey is impossible.

        HOW TO INVESTIGATE:
        1. Examine the four suspects and their statements.
        2. View the museum map to check minimum travel times.
        3. Calculate how long each suspect claims their journey took.
        4. Compare their claimed duration with the minimum travel time.
        5. Accuse the suspect whose claimed duration is too short.

        SCORING:
        Correct accusation: +100 points
        Wrong accusation: 0 points

        You get only ONE accusation per investigation.

        After your accusation, the actual inconsistent suspect
        and the evidence will be revealed.

        Good luck, Detective!

        ===============================================================
        """)

            print(
            "NOTE: Generated journeys may include up to 5 extra minutes "
            "beyond the minimum travel time.\n"
            "An alibi is inconsistent only when the claimed time "
            "is shorter than the minimum required time."
                )

        elif option == "3":
            sys.exit()

        else:
            print("Select a valid option!")


def investigation_menu(case):
    while True:
        print("""\n
            1. Examine Suspects
            2. View Museum Map
            3. Make Accusation
            4. Exit Investigation
            \n"""
        )

        option = input("Enter an option \n(1, 2, 3, 4)\n >>> ").strip()

        if option == "1":
            display_suspects(case)

        elif option == "2":
            display_map(case)

        elif option == "3":
            answer = analyse_case(case)
            user_ans = user_input(case)

            answer = answer.strip().casefold()
            user_ans = user_ans.strip().casefold()

            result_path = result(answer, user_ans)
            if result_path == True:
                print("\nBRAVO! Right Answer\n")
            else:
                print("\nUGH! Wrong Answer\n")

            reveal_ans(case, answer)
            points = point_evaluation(result_path)

            return points

        elif option == "4":
            print("You have exited the investigation! ")
            return

        else:
            print("Select a valid option!")


def user_input(case):
    suspects_list = []

    for suspect in case["suspects"]:
        suspects_list.append(suspect["name"].strip().casefold())

    while True:
        user_suspect = input("\nWhich suspect has an inconsitent alibi? ")

        if user_suspect.strip().casefold() not in suspects_list:
            print("Invalid suspect! Choose one of the four suspects.")
            continue

        return user_suspect


def result(answer, user_ans):
    return answer == user_ans


def point_evaluation(result_path):
    if result_path == True:
        points = 100
    else:
        points = 0

    return points


def reveal_ans(case, answer):
    for suspect in case["suspects"]:
        if suspect["name"].casefold() == answer.casefold():
            name = suspect["name"]

            start = suspect["from"]
            end = suspect["to"]

            departure = suspect["departure"]
            arrival = suspect["arrival"]

            elapsed = calc_elapsed_time(departure, arrival)
            required = get_travel_time(case, start, end)
            difference = required - elapsed

            print(f"Inconsistent suspect: {name}")
            print()
            print(f"The {name} traveled from {start} to {end}.")
            print(f"Departure: {departure}")
            print(f"Arrival: {arrival}")
            print()
            print(f"Claimed journey: {elapsed} minutes")
            print(f"Minimum required: {required} minutes")
            print(f"Difference: {difference} minutes")

            return #To tell that you have found the suspect and no longer need to search for it


def display_suspects(case):
    print("\n?_?_?_?_?_?_?_?_?_?_?_?___SUSPECTS___?_?_?_?_?_?_?_?_?_?_?_?_?\n")

    for suspect in case["suspects"]:
        print(
            f"{suspect['name']}: I went from "
            f"{suspect['from']} : {suspect['departure']}, "
            f"to {suspect['to']} : {suspect['arrival']}.\n"
        )

    print("________________________________________________________")


def display_map(data):
    print("\n<--------------------MAP-------------------->\n")

    for time in data["travel_times"]:
        print(
            f"From {time['from']} --> {time['to']}, "
            f"it takes {time['minutes']} minutes.\n"
        )

    print("\n<------------------------------------------->\n")


def generate_case(data):
    suspects_list = []
    selected_suspect = random.choice(data["suspects"])

    for suspect in data["suspects"]:
        route = random.choice(data["travel_times"])
        mins = route["minutes"]

        d_time = generate_time()

        if selected_suspect["name"] == suspect["name"]:
            a_time = d_time + random.randint(1, int(mins)-1)

        else:
            a_time = d_time + random.randint(mins, int(mins)+5)

        new_suspect = {
            "name": suspect["name"],
            "from": route["from"],
            "to": route["to"],
            "departure": format_time(d_time),
            "arrival": format_time(a_time)
        }

        suspects_list.append(new_suspect)

    new_case = data.copy()
    new_case["suspects"] = suspects_list

    analyse_case(new_case)

    return new_case


def generate_time():
    time = random.randint(540, 1020)
    return time


def format_time(time):
    hours = time // 60
    mins = time % 60

    return f"{hours:02d}:{mins:02d}"


def analyse_case(case):
    inconsistent = []

    for suspect in case["suspects"]:
        elapse = calc_elapsed_time(
            suspect["departure"],
            suspect["arrival"]
        )

        travel = get_travel_time(
            case,
            suspect["from"],
            suspect["to"]
        )

        result = check_alibi(elapse, travel)

        if result == False:
            inconsistent.append(suspect["name"])

    if len(inconsistent) != 1:
        raise ValueError("Case must have excatly one inconsistent alibi!")

    return inconsistent[0]


def calc_elapsed_time(departure, arrival):
    if validate_time(departure) is True and validate_time(arrival) is True:

        hour_d, mins_d = departure.split(":")
        departure_mins = (int(hour_d)*60 + int(mins_d))

        hour_a, mins_a = arrival.split(":")
        arrival_mins = (int(hour_a)*60 + int(mins_a))

        if arrival_mins < departure_mins:
            raise ValueError("Arrival cannot occur before departure")

        return arrival_mins - departure_mins

    else:
        raise ValueError("Arrival/Departure time is Invalid!")


def validate_time(time_string):
    if len(time_string) == 5 and time_string[2] == ":":
        hours, mins = time_string.split(":")

        if len(hours) == 2 and hours.isdigit() and len(mins) == 2 and mins.isdigit():
            if 0 <= int(hours) <= 23 and 0 <= int(mins) <= 59:
                return True

    return False


def get_travel_time(data, start, end):
    for route in data["travel_times"]:
        if (
            (route["from"] == start and route["to"] == end)
            or
            (route["from"] == end and route["to"] == start)
        ):
            return route["minutes"]

    raise ValueError("Route not found")


def check_alibi(elapse, travel):
    return elapse >= travel


if __name__ == "__main__":
    main()
