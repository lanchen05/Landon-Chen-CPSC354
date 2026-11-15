
# Lambda Calculus Interpreter

This interpreter evaluates lambda calculus expressions and reduces them to their normal form. It parses the input, does beta reduction, and outputs the fully reduced expression.

## Usage

```bash
python interpreter.py <expression>
```

The program is executed using either a filename or
expression, but for the sake of this assignment testing
will be done through expressions.

## What Changed: Full Reduction

Updated the interpreter to do full reduction to normal form. The main changes are:

### 1. Evaluating Both Sides of Applications

**Before**: When you had an application like `(e1 e2)` where `e1` wasn't a lambda, it wouldn't evaluate `e2` first.

**Now**: Both sides get evaluated:

```python
e2 = evaluate(tree[2])
return ('app', e1, e2)
```

This makes sure nested applications get fully reduced.

### 2. Evaluating Lambda Bodies

**Before**: Lambda expressions like `\x.e` were returned as-is without evaluating what's inside.

**Now**: The body gets evaluated too:

```python
elif tree[0] == 'lam':
    return ('lam', tree[1], evaluate(tree[2]))
```

This is important because without it, expressions inside lambdas wouldn't get reduced. For example, `(\x.(\y.y) x)` wouldn't fully reduce.

## Impact

With these changes, the interpreter actually reduces everything to normal form. Before, it would only do partial evaluation and leave some reducible parts in the output. Now it fully simplifies everything.
