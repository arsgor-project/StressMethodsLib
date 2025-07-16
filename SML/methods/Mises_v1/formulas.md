[Parameters]
Деталь : det-{Название детали}
Зона : zone-{Номер зоны}
Номер КЭ : FE_list-{}
Определяющий РС : CritLC_Name_list-{}
t, [мм] : th-{t}
q_vonMises : qVMMax-{q_{vm}}_{max}
sigma_vonMises : sVM-\sigma_{vm}
sigma_вр : sVr-\sigma_{вр}
Коэффициент запаса : safetyFactor-{КЗ}
[Formulas]
$ {Деталь - /pdet ,\; Зона - /pzone} $
$ {q_{vm}}_{max}=/pqVMMax\;[Н]$
$ \sigma_{vm}=\frac{/pqVMMax}{/pth}={/psVM}\;[МПа]$
$ {КЗ}=\frac{/psVr}{/psVM}={/psafetyFactor} $
