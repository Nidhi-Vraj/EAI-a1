"""
# assign.py : Assign people to teams
#
# Code by: Nidhi Vraj Sadhuvala, Aditi Soni, Srinivas Vaddi, Username - nsadhuva-adisoni-svaddi
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#
"""
#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: Nidhi Vraj Sadhuvala, Aditi Soni, Srinivas Vaddi, Username - nsadhuva-adisoni-svaddi
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#
import sys
import random
import itertools


class User:
    """
    Class for every user in the input file
    """

    def __init__(self, user):
        self.chosen = []
        self.dont_want_to_work_with = []
        self.team_size = 0
        self.any_random = 0
        self.worthy = []
        self.worthy_teams = []
        dets = user.strip().split(" ")
        self.username = dets[0].strip()
        if "xxx" in dets[1].strip().split("-"):
            self.any_random = dets[1].strip().split("-").count("xxx")
            self.chosen = list(
                filter(
                    ("xxx").__ne__,
                    dets[1].strip().split("-")))
        elif "zzz" in dets[1].strip().split("-"):
            self.any_random = dets[1].strip().split("-").count("zzz")
            self.chosen = list(
                filter(
                    ("zzz").__ne__,
                    dets[1].strip().split("-")))
        else:
            self.chosen = dets[1].strip().split("-")
        self.team_size = len(dets[1].strip().split("-"))
        if dets[2].strip() == "_":
            self.dont_want_to_work_with = []
        else:
            self.dont_want_to_work_with = dets[2].split(",")

    def __str__(self):
        """
        returns the user details as a string
        """
        return "\nChosen teammates : {}\ndont_want_to_work_with : {}\nTeam-size : {}\nany_random : {}\all_users\all_users".format(
            self.chosen, self.dont_want_to_work_with, self.team_size, self.any_random)

    def no_wanted(self):
        """
        what is the desired team size
        """
        return self.team_size

    def chosen_team(self):
        """
        who are the people this user wants to work with apart from himself
        """
        if len(self.chosen) > 0:
            return self.chosen[1:]
        else:
            return []

    def gen_worthy_teams(self):
        """
        what are all the possible teams we have for this given user and his worthy teammates
        """
        self.worthy_teams.extend(list(itertools.combinations(self.worthy, 3)))
        self.worthy_teams.extend(list(itertools.combinations(self.worthy, 2)))
        self.worthy_teams.extend(list(itertools.combinations(self.worthy, 1)))


def calculate_cost(all_user_dict, team):
    """
    Cost    :
        action                  cause                                               cost

        grading                                                                     5 mins
        mail to professor       incorrect team size                                 2 mins
        integrity session       sharing code (different teammate than requested)    5% probability and 60 mins - 3mins
        speaking with Dean      when teamed with dont-want-to-work-with             10 mins

    :param all_user_dict:
    :return:
    """
    grading_time = 5
    mail_time = 2
    integrity_session_time = 3
    dean_time = 10
    integrity_session_needed = 0
    no_dont_want_to_work_with = 0
    wrong_team_sizes = 0
    # p#print.p#print(locals())
    for i in team.current_team:
        # p#print.p#print(all_user_dict[i])
        if all_user_dict[i].team_size != len(team.current_team):
            #print("{} did not get desired team size, adding time to email".format(i))
            wrong_team_sizes += 1
        for j in all_user_dict[i].chosen:
            if j not in team.current_team:
                # print(
                # "{} did not get desired team member, adding time for integrity session".format(i))
                integrity_session_needed += 1
        # #print(i, all_user_dict[i]["dont_want_to_work_with"])
        if any(
                [True for j in team.current_team if j in all_user_dict[i].dont_want_to_work_with]):
            # print(
            # "{} got dont_want_to_work_with team member, adding time to speak with dean".format(i))
            no_dont_want_to_work_with += 1
    time_per_team = grading_time + wrong_team_sizes * mail_time\
        + integrity_session_needed * integrity_session_time \
        + dean_time * no_dont_want_to_work_with
    return {
        "dont_want_to_work_with": no_dont_want_to_work_with,
        "wrong_team_sizes": wrong_team_sizes,
        "time_per_team": time_per_team,
        "integrity_session_needed": integrity_session_needed
    }


class Team:
    """
    All users eventually are teamed up.
    and this is the class where each teams cost is calculated
    """

    def __init__(self, teammates=[]):
        """
        can take a list of users as input
        """
        # list of all members in team as instances of User
        self.current_team = []

        # cost until this point
        self.previous_cost = 0

        # How many members in this team got wrong teamsizes
        self.wrong_team_sizes = 0

        # How many dont_want_to_work_with members are here?
        self.dont_want_to_work_with = 0

        # how many need integrity session? probably gonna copy if they didnt
        # get someone they asked for
        self.integrity_session_needed = 0

        # current team size
        self.team_size = 0

        # how many of the users are chosen?
        self.chosen = 0

        # whats the max group size of all preferences
        self.max_team_size = 0

        # whats the min group size of all preferences
        self.min_team_size = 0

        # what is the team name?
        self.team_name = ""

        # default maximum team size
        self.default_max_team_size = 3

        # whom can I oboard without having trouble with anyone
        self.all_safe_wanted = []

        # whom shall I never onboard to avoid dean time
        self.all_dont_want_to_work_with = []

        # wanted common
        self.all_wanted = []

        # dont_want_to_work_with
        # has_dont_want_to_work_with = []

        self.sizes = {1: [], 2: [], 3: []}

        for i in teammates:
            self.current_team.append(i)
        self.team_size = len(self.current_team)
        self.validate_team()
        self.set_team_name()
        # self.set_max_team_size()
        # self.set_min_team_size()
        self.set_all_safe_dont_want_to_work_with()

    def __str__(self):
        """
        return team name
        """
        return self.team_name

    def add_teammate(self, username):
        """
        add a user to existing team
        """
        self.current_team.append(username)
        self.team_size = len(self.current_team)
        self.validate_team()
        self.set_team_name()
        # self.set_max_team_size()
        # self.set_min_team_size()
        self.set_all_safe_dont_want_to_work_with()

    def remove_teammate(self, username):
        """
        remove a given user from the team
        """
        self.current_team.remove(username)
        self.team_size = len(self.current_team)
        self.validate_team()
        self.set_team_name()
        # self.set_max_team_size()
        # self.set_min_team_size()
        self.set_all_safe_dont_want_to_work_with()

    def is_member(self, username):
        """
        is this user a member of this given team
        """
        return True if username in self.current_team else False

    def set_team_name(self):
        """just set the team name already"""
        self.team_name = "-".join([i.username for i in self.current_team])

    def set_all_safe_dont_want_to_work_with(self):
        """
        who does all these teammates dont want to work with
        """
        self.all_dont_want_to_work_with = list(
            set(self.all_dont_want_to_work_with) - set(self.all_wanted))

    def validate_team(self):
        """
        cost function: critical part of this code
        # get the total time taken
        # Cost    :
        #   action                  cause                                               cost
        #
        #   grading                                                                     5 mins
        #   mail to professor       incorrect team size                                 2 mins
        #   integrity session       sharing code (different teammate than requested)    5% probability and 60 mins - 3mins
        # speaking with Dean      when teamed with dont-want-to-work-with
        # 10 mins
        """
        grading_time = 5
        mail_time = 2
        integrity_session_time = 3
        dean_time = 10

        for i in self.current_team:
            # if someone has a different team-size priority than the current
            # team size
            if i.team_size != self.team_size:
                # #print(
                #     "{} did not get desired team size, adding time to email".format(
                #         i.username))
                self.wrong_team_sizes += 1
                self.sizes[i.team_size] = i
            # for each of my wanted
            for j in i.chosen_team():

                # if they are not here I probably will share code
                if j not in [g.username for g in self.current_team]:
                    # #print(
                    #     "{} did not get desired team member, adding time for integrity session".format(
                    #         i.username))
                    self.integrity_session_needed += 1

            # if there is anyone in the current team that I dont want to work
            # with, I will go speak to dean
            for j in self.current_team:
                if j.username in i.dont_want_to_work_with:
                    # #print(
                    #     "{} got dont_want_to_work_with team member, adding time to speak with dean".format(
                    #         i.username))
                    self.dont_want_to_work_with += 1
                    self.all_dont_want_to_work_with.append(j)

        self.time_per_team = grading_time +\
            self.wrong_team_sizes * mail_time +\
            self.integrity_session_needed * integrity_session_time +\
            dean_time * self.dont_want_to_work_with


class Sol:
    """
    All teams together must form a solution.
    """

    def __init__(self, all_users, teams=[]):
        """
        initialize the soln object with a list of teams
        """
        # print(teams)
        self.teams = teams
        self.cost = sum([i.time_per_team for i in self.teams])
        self.name = " ".join([i.team_name for i in self.teams])
        self.users = []
        self.update()
        self.all_users = all_users
        self.needed_members = []

    def is_soln(self):
        """
        is the current solution a final solution?

        to answer that we must check -> is every user a part of some team of this solution?
        """
        if sorted([i.username for i in self.all_users]) == sorted(
                [i.username for i in self.users]):
            return True
        else:
            return False

    def add_member(self, team):
        """
        add a team to this solution
        """
        self.teams.append(team)
        self.update()

    def needed_members_list(self):
        """
        whom do we need to make this solution a complete solution?
        """
        # print([i.username for i in self.all_users if i not in self.users])
        return [i for i in self.all_users if i not in self.users]

    def update(self):
        """
        modifications to various sections of this code must also reflect in the object, so just update them
        """
        self.cost = sum([i.time_per_team for i in self.teams])
        self.name = " ".join([i.team_name for i in self.teams])
        self.users = []
        for i in self.teams:
            # print(i)
            [self.users.append(j) for j in i.current_team]

    def __str__(self):
        """
        return the name of each team as a part of the solution
        """
        return "Teams are - " + self.name + " and cost is " + str(self.cost)


def select_random_teams(list_of_all, size_of_team):
    """
    Only makes random teams of given size.
    Needed for a starter
    """
    teams = []
    random.shuffle(list_of_all)
    for i in range(0, len(list_of_all), size_of_team):
        team_one = Team(list_of_all[i:i + size_of_team])
        teams.append(team_one)
    return teams


def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any_random extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any_random global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    all_user_dict = {}
    for user in open(input_file).readlines():
        user_dict = User(user)
        all_user_dict.update({user_dict.username: user_dict})

    all_users = list(all_user_dict.values())
    solution_object = Sol(all_users, select_random_teams(all_users, 3))
    # yield something
    yield ({"assigned-groups": [e.team_name for e in solution_object.teams], "total-cost": solution_object.cost})

    for i in list(all_user_dict.values()):
        for j in list(all_user_dict.values()):
            if i == j:
                continue
            if j in i.dont_want_to_work_with or i in j.dont_want_to_work_with:
                continue
            else:
                # mark worthy candidate for user
                i.worthy.append(j)
    for i in list(all_user_dict.values()):
        i.gen_worthy_teams()
    super_worthy_teams = []

    for i in list(all_user_dict.values()):
        for j in i.worthy_teams:
            super_worthy_teams.append(j)
    super_worthy_teams = list(set(super_worthy_teams))
    g_min = 0
    while True:
        random.shuffle(super_worthy_teams)
        solution_object = Sol(list(all_user_dict.values()), [])

        while not solution_object.is_soln():

            is_present = False
            random_choice_team = random.choice(super_worthy_teams)
            for i in random_choice_team:
                if i in solution_object.users:
                    is_present = True
                    break
            if not is_present:
                solution_object.add_member(Team(random_choice_team))
        #         print("Team  cost is - ",solution_object.cost)
        if g_min == 0:
            g_min = solution_object.cost
        if solution_object.cost < g_min:
            g_min = solution_object.cost
            # old_sol.append(solution_object.teams)
            random.shuffle(super_worthy_teams)
            yield ({"assigned-groups": [e.team_name for e in solution_object.teams], "total-cost": solution_object.cost})
        random.shuffle(super_worthy_teams)


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\all_users" +
              "\all_users".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \all_users" % result["total-cost"])
