from populator import populator


def argumentparser():
    try:
        import argparse
        import sys
    except:
        print("\nxx Error importing arparse or sys module\n")
        exit(1)

    parser = argparse.ArgumentParser(
        description='To process tables in images.', prog='populator')
    parser.add_argument(
        '-p', '--path', help='Path for the tabular source image')
    parser.add_argument('-db', '--database',
                        help='Name of database')
    parser.add_argument(
        '-t', '--table', help='Name of the table')

    if len(sys.argv) > 1:
        args = parser.parse_args()
        path = args.path
        try:
            f = open(path)
            f.close()
        except FileNotFoundError:
            print("File not accessible")
            print("\n### EXITING ###")
            exit(1)
        database_name = args.database if len(
            args.database) != 0 else input("Enter the name of database: ")
        table_name = args.table if len(args.table) != 0 else input(
            "Enter the name of table: ")
    else:
        path = input("Enter image path: ")
        try:
            f = open(path)
            f.close()
        except FileNotFoundError:
            print("\nxx File not accessible\n")
            exit(1)
        database_name = input("Enter the name of database: ")
        table_name = input("Enter the name of table: ")
    return (path, database_name, table_name)


def main():
    print("\n==================== SEQUEL INJECTOR ====================\n")
    path, database_name, table_name = argumentparser()
    populator(path, database_name, table_name)
    print("\n=========================================================\n")


if __name__ == "__main__":
    main()
