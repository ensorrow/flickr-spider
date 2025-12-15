while True:
    try:
        expr = input("Enter expression: ")
        if expr.lower() in ('exit', 'quit'):
            break
        result = eval(expr)
        print(result)
    except ZeroDivisionError:
        print("Error: Division by zero")
    except (SyntaxError, NameError, TypeError):
        print("Error: Invalid expression")
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")
