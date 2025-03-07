from cloc import CLOC
import json

if __name__ == "__main__":
    result = json.loads(CLOC().add_flag("--by-file")
                    .add_flag("--json")
                    .add_option("--timeout", 30)
                    .set_working_directory('./')
                    .add_argument('b95e1a662d44ad70dda1744baf6cd91606fc6702')
                    .execute())

    print(json.dumps(result, indent=4))