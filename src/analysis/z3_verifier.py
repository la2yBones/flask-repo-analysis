from z3 import Bool, Solver, And, Not, Implies, sat

def verify_route_permission(user_role, required_role):
    """
    验证权限逻辑。
    假设：admin 角色包含所有权限。
    """
    IsAdmin = Bool('IsAdmin')
    IsUser = Bool('IsUser')
    HasAccess = Bool('HasAccess')

    s = Solver()
    
    # 规则1：如果是 Admin，一定有 HasAccess
    s.add(Implies(IsAdmin, HasAccess))
    
    # 规则2：如果只是 User 且不是 Admin，没有 HasAccess (模拟一个潜在 Bug 逻辑)
    s.add(Implies(And(IsUser, Not(IsAdmin)), Not(HasAccess)))

    # 检测目标：是否存在一种情况，用户既是 User 又是 Admin，但被拒绝访问？
    s.add(IsAdmin == True)
    s.add(IsUser == True)
    s.add(HasAccess == False)

    if s.check() == sat:
        return f"Logic Conflict Found: {s.model()}"
    return "Permission logic consistent."