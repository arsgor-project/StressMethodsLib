[Parameters]
Деталь : det
Зона : zone
Номер КЭ : FE_list
Определяющий РС : CritLC_Name_list
t, [мм] : th
q_vonMises : qVMMax
sigma_vonMises : sVM
sigma_вр : sVr
Коэффициент запаса : safetyFactor
[Formulas]
$ {Деталь - /pdet ,\; Зона - /pzone} $
${q_{vm}}_{max}=/pqVMMax $
$ \sigma_{vm}=\frac{/pqVMMax}{/pth}={/psVM} $
$ {КЗ}=\frac{/psVr}{/psVM}={/psafetyFactor} $
