from ava_prime_integration import AvaPrimeWorkflows, UserManager, Role


def main():
    um = UserManager()
    user = um.add_user("briefing_bot", Role.DEVELOPER)
    workflows = AvaPrimeWorkflows()
    briefing = workflows.generate_morning_briefing(user)
    print("== Morning Briefing ==")
    print(briefing)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

