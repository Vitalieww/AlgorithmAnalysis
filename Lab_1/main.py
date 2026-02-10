from empirical_analysis import MultiEmpiricalTest, EmpiricalTest
from fibonacci_methods.recursive_method import recursive_method
from fibonacci_methods.dynamic_method import dynamic_method
from fibonacci_methods.matrix_power_method import matrix_power_method
from fibonacci_methods.binet_method import binet_method
from fibonacci_methods.fast_doubling_method import fib_fast_doubling


limited_scope = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45]
big_scope = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]



# Empirical test for recursive Fibonacci method
#
# test_recursive = EmpiricalTest(recursive_method)
# test_recursive.overall_test(limited_scope,repetitions=1)
# #----------------------------------------------------------

# Empirical test for dynamic Fibonacci method

# test_dynamic = EmpiricalTest(dynamic_method)
# test_dynamic.overall_test(big_scope, repetitions=1)
# #----------------------------------------------------------

# Empirical test for matrix power Fibonacci method

# test_matrix_power = EmpiricalTest(matrix_power_method)
# test_matrix_power.overall_test(big_scope, repetitions=10)
# #----------------------------------------------------------

# Empirical test for Binet's formula Fibonacci method

# test_binet = EmpiricalTest(binet_method)
# test_binet.overall_test(big_scope, repetitions=10)
# #----------------------------------------------------------

# Empirical test for Fast Doubling Fibonacci method

# test_doubling = EmpiricalTest(fib_fast_doubling)
# test_doubling.overall_test(big_scope, repetitions=10)
# #----------------------------------------------------------

# Empirical test for all methods together

multi_test = MultiEmpiricalTest([
    # (recursive_method, "Recursive"),
    dynamic_method,
    matrix_power_method,
    binet_method,
    fib_fast_doubling
])

multi_test.overall_test(big_scope,repetitions=10)