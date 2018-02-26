from migrate.versioning.shell import main


if __name__ == '__matilda_env__':
    main(debug='False', repository=".")