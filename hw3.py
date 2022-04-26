import streamlit as st

no_clairvoyance = 80000

natural_possibility_of_storm = st.number_input("natural_possibility_of_storm",min_value=0.0, max_value=1.0, value=0.5)

#sensitivity = st.number_input("sensitivity of the model",min_value=0.0, max_value=1.0, value=0.8)
#specificity = st.number_input("specificity of the model",min_value=0.0, max_value=1.0, value=0.8)

sensitivity = 0.85
specificity = 0.83

p_s = natural_possibility_of_storm * sensitivity + (1 - natural_possibility_of_storm) * (1 - sensitivity)
p_ns = (1 - natural_possibility_of_storm) * specificity + natural_possibility_of_storm * (1 - specificity)

p_s_ds = natural_possibility_of_storm * sensitivity / p_s
p_ns_dns = (1 - natural_possibility_of_storm) * specificity / p_ns

chance_of_botrytis = st.number_input("chance_of_botrytis",min_value=0.0, max_value=1.0, value=0.1)

chance_of_sugar_levels_no = st.number_input("chance_of_sugar_levels_no",min_value=0.0, max_value=1.0, value=0.6)
chance_of_sugar_levels_typical = st.number_input("chance_of_sugar_levels_typical",min_value=0.0, max_value=1.0, value=0.3)
chance_of_sugar_levels_high = st.number_input("chance_of_sugar_levels_high",min_value=0.0, max_value=1.0, value=0.1)

nh_ns = 80000 * chance_of_sugar_levels_no + 117500 * chance_of_sugar_levels_typical + 125000 * chance_of_sugar_levels_high

nh_s = 275000 * chance_of_botrytis + 35000 * (1 - chance_of_botrytis)

nh = p_s * nh_s + p_ns * nh_ns

# Even the accuracy of model is poor, the exception will not be worse(if we don't consider the cost of model)
# if we buy, and model say it will storm
DS_H = 80000
DS_NH = p_s_ds * nh_s + (1 - p_s_ds) * nh_ns

# depend on the change of possibilitiy of chance_of_botrytis
if DS_H >= DS_NH:
    DS = DS_H
    choice1="We should harvest"
else:
    DS = DS_NH
    choice1="We should not harvest"

# if we buy, and model say it will not storm
DNS_H = 80000
DNS_NH = p_ns_dns * nh_ns + (1 - p_ns_dns) * nh_s

# depend on the change of possibilitiy of chance_of_botrytis
if DNS_H >= DNS_NH:
    DNS = DNS_H
    choice2="We should harvest"
else:
    DNS = DNS_NH
    choice2="We should not harvest"

E_Value = DS * p_s + DNS * p_ns

Accepet_price = E_Value - no_clairvoyance

print("The E_Value is:")
print(E_Value)

# actually is always larger
if Accepet_price >= 0:
    choice3="We should buy the clairvoyance less than the cost of:"
    print(Accepet_price)
else:
    print("We should not buy the clairvoyance")

st.subheader('The E_Value is: ')
st.write(E_Value)

st.subheader('We should buy the clairvoyance less than the cost of: ')
st.write(Accepet_price)

st.subheader('If the model say it will strom： ')
st.write(choice1)

st.subheader('If the model say it will not strom： ')
st.write(choice2)