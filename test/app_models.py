from decimal import Decimal
from sqlalchemy import JSON, BigInteger, Boolean, Column, Date, Float, Identity, Index, Integer, Numeric, String, Table, Unicode, ForeignKey, UniqueConstraint, DateTime, Text, SMALLINT
from sqlalchemy.orm import declarative_base, relationship

import enum

Base = declarative_base()
metadata = Base.metadata

class UserRole(enum.Enum):
    super_admin = "Finalyca Admin"
    org_admin = "Organization Admin"
    guest = "Guest"
    user = "User"
    api = "API"

class ScreenerAccess(enum.Enum):
    # Anything created under finalyca admin will be public
    public = "Public"
    # screeners created by org customers e.g. hdfc sec
    organization = "Organization"
    # # screeners created by org customers for small segments
    # restricted = "Restricted"
    # screeners created by users for personal use
    personal = "Personal"

class Screener(Base):
    __tablename__ = 'Screener'
    
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, nullable=False, default=True)
    edit_history = Column(JSON)
    name = Column(String(100))
    query_json = Column(Text)
    scope = Column(String(100))

    def __str__(self) -> str:
        return self.name

class Organization(Base):
    __tablename__ = 'Organization'
    
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, nullable=False, default=True)
    edit_history = Column(JSON)

    name = Column(String(100), nullable=False)
    license_expiry_date = Column(Date, nullable=False)
    # user_count = Column(Integer, nullable=False, default=1)
    api_count = Column(Integer, nullable=False, default=0)
    admin_name = Column(String(100), nullable=False)
    admin_email = Column(String(50), nullable=False)
    admin_mobile = Column(String(20), nullable=False)
    has_api = Column(Boolean, nullable=False, default=False)
    is_whitelabelled = Column(Boolean, nullable=False, default=False)
    can_restrict_menu = Column(Boolean, nullable=False, default=False)
    can_restrict_data = Column(Boolean, nullable=False, default=False)
    can_export = Column(Boolean, nullable=False, default=False)
    export_fund_count = Column(Integer, nullable=False, default=0)
    can_create_screener = Column(Boolean, nullable=False, default=True)
    arn_nr = Column(String(100), comment="AMFI Registered Number for distribution.")
    can_transact = Column(Boolean, nullable=False, default=True)
    amc_sebi_nr = Column(String(100), comment="sebi_nr of the AMC if this organization is an AMC")
    can_add_fund_data = Column(Boolean, nullable=False, default=False, comment="relavent only if valid amc_sebi_nr")
    can_add_content = Column(Boolean, nullable=False, default=False, comment="relavent only if valid amc_sebi_nr")

class FundTransaction(Base):
    __tablename__ = 'FundTransaction'
    
    id = Column(Integer, primary_key=True)

    is_active = Column(Boolean, nullable=False, default=True)
    edit_history = Column(JSON)
    amc_id = Column(Integer, index=True)
    fund_id = Column(Integer, index=True)
    can_transact = Column(Boolean)
    is_pms_bazaar_distributor = Column(Boolean)
    transaction_settings = Column(JSON)
    digital_enabler = Column(String(100))

# organization wide defaults
class OrganizationSettings(Base):
    __tablename__ = 'OrganizationSettings'
    
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, nullable=False, default=True)
    edit_history = Column(JSON)
    organization_id = Column(Integer, ForeignKey(u'Organization.id'), index=True)
    white_label_settings = Column(JSON, comment="has logo, app name, color schemes, fonts, disclaimer etc")
    empanelment_settings = Column(JSON, comment="list of amc and/or fund for which fund is empanelled")
    export_settings = Column(JSON, comment="list of funds that can be exported. upper limit defined by Organization.export_fund_count")

    organization = relationship(u'Organization')

class UserSubRole(Base):
    __tablename__ = 'UserSubRole'

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, nullable=False, default=True)
    edit_history = Column(JSON)
    name = Column(String(100), nullable=False)
    organization_id = Column(Integer, ForeignKey(u'Organization.id'), index=True)
    can_export = Column(Boolean)
    can_view_fund = Column(Boolean)
    view_fund_include_list = Column(JSON, comment="amc/fund list. show from the list if defined else show all funds.")
    view_fund_exclude_list = Column(JSON, comment="amc/fund list. hide from the list if defined else show all funds.")
    can_access_screener = Column(Boolean)
    screener_include_list = Column(JSON, comment="screener list. if defined show selected, else show everything")
    screener_exclude_list = Column(JSON, comment="screener list. if defined hide selected, else show everything")
    can_transact_fund = Column(Boolean)
    transaction_fund_include_list = Column(JSON, comment="amc and/or fund list. show only these ones if defined else show everything")
    transaction_fund_exclude_list = Column(JSON, comment="list of amc and/or fund")
    can_add_funds = Column(Boolean)
    can_add_funds_data = Column(Boolean)
    can_add_content = Column(Boolean)

    organization = relationship(u'Organization')

class OrganizationSubroles(Base):
    __tablename__ = "OrganizationSubroles"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey(u'Organization.id'), index=True)
    user_subrole_id = Column(Integer, ForeignKey(u'SubRole.id'), index=True)
    licence_count = Column(Integer)


class User(Base):
    __tablename__ = 'User'
    
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, nullable=False, default=True)
    edit_history = Column(JSON)

    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    mobile = Column(String(20), nullable=False)
    organization_id = Column(Integer, ForeignKey(u'Organization.id'), index=True)
    # role_id = Column(Integer, ForeignKey(u'Role.id'), index=True, comment="this will be visible only to super admin.")
    role_id = Column(String(20), default=UserRole.guest.name, comment="this will be visible only to super admin.")
    sub_role_id = Column(Integer, ForeignKey(u'SubRole.id'), index=True, comment="by default this will be visible to org-admin.")
    designation = Column(String(50))
    address = Column(String(500))
    city = Column(String(100))
    state = Column(String(100))
    pin_code = Column(String(10))
    birth_date = Column(Date, nullable=False)
    is_locked = Column(Boolean, nullable=False)
    last_login_at = Column(DateTime, nullable=False)
    referred_by_id = Column(Integer, ForeignKey(u'User.id'))
    reference_code = Column(String(50))
    login_count = Column(Integer)
    activation_code = Column(String(50))
    otp = Column(Integer)
    session_id = Column(String(50))

    Account_Locked_Till_Date = Column(Date)
    Salutation = Column(Unicode(5), nullable=False)
    First_Name = Column(Unicode(20), nullable=False)
    Middle_Name = Column(Unicode(20), nullable=False)
    Last_Name = Column(Unicode(20), nullable=False)
    Gender = Column(SMALLINT, nullable=False)
    Marital_Status = Column(SMALLINT, nullable=False)
    Secret_Question_Id = Column(BigInteger)
    Hint_Word = Column(Unicode(50))
    Secret_Answer = Column(Unicode(100))
    Login_Failed_Attempts = Column(SMALLINT, nullable=False)
    
    referred_by = relationship(u'User', foreign_keys=[referred_by_id])
    organization = relationship(u'Organization')
    # role = relationship(u'Role')
    sub_role = relationship(u'SubRole')

class APIKey(Base):
    __tablename__ = 'APIKey'
    
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, nullable=False, default=True)
    edit_history = Column(JSON)
    name = Column(String(100), nullable=False)
    organization_id = Column(Integer, ForeignKey(u'Organization.id'), index=True)
    api_key = Column(String(100), nullable=False, comment="this has to be stored after hashing as this is like password.")        
    is_locked = Column(Boolean, nullable=False)
    last_accessed_at = Column(DateTime, nullable=False)

    organization = relationship(u'Organization')


# class Menu(Base):
#     __tablename__ = 'Menu'
    
#     Menu_Id = Column(Integer, primary_key=True)
#     Menu_Name = Column(Unicode(50), nullable=False)
#     Application_Id = Column(BigInteger, nullable=False)
#     Parent_Id = Column(BigInteger, nullable=False)
#     Menu_Order = Column(SMALLINT, nullable=False)
#     Menu_Level = Column(SMALLINT, nullable=False)
#     Is_Active = Column(Boolean, nullable=False)
#     Created_By_User_Id = Column(BigInteger, nullable=False)
#     Created_Date_Time = Column(DateTime, nullable=False)
#     Menu_URL = Column(Unicode(100))
#     Modified_By_User_Id = Column(BigInteger)
#     Modified_Date_Time = Column(DateTime)
#     CSS_Class = Column(String(500))
#     CSS_Icon = Column(String(50))
#     Angular_CSS_Icon = Column(String(50))
#     Angular_Menu_URL = Column(String(100))

# class RoleMenuPermission(Base):
#     __tablename__ = 'RoleMenuPermission'

#     RoleMenuPermission_Id = Column(Integer, primary_key=True)
#     Role_Id = Column(BigInteger, nullable=False)
#     Menu_Id = Column(BigInteger, nullable=False)
#     View_Access = Column(Boolean, nullable=False)
#     Add_Access = Column(Boolean, nullable=False)
#     Modify_Access = Column(Boolean, nullable=False)
#     Delete_Access = Column(Boolean, nullable=False)
#     All_Access = Column(Boolean, nullable=False)
#     Is_Visible = Column(Boolean, nullable=False)
#     Is_Disabled = Column(Boolean, nullable=False)
#     Is_Active = Column(Boolean, nullable=False)
#     Created_By_User_Id = Column(BigInteger, nullable=False)
#     Created_Date_Time = Column(DateTime, nullable=False)
#     ModifiedBy_User_Id = Column(BigInteger)
#     Modified_Date_Time = Column(DateTime)
