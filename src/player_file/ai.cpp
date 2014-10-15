#include "basic.h"
#include<iostream>
#include<cmath>
#include<vector>
#include<iterator>
#include<algorithm>
#include<functional>

// Remove this line if you konw C++, and don't want a dirty namespace
using namespace teamstyle16;

const char * GetTeamName()
{
    return "来瓶酱油";  // Name of your team
}

const GameInfo *INFO = Info();
int enemy_num,DISTANCE;
State * enemy_element;
int (*command)[2]= new int[INFO->element_num][2];
double parameter[10];
int cargo_index[2];  //两个补给基地的     初始化为-2，-1表示在生产
int resource_defender[2];  //守在资源点潜艇，初始化为-2，-1表示在生产
int base_defender[2];      //留守基地的潜艇，初始化为 -2，-1表示在生产
Position origin_target[5];  //中三路驱逐舰+潜艇+飞机*2+侦察机,两侧飞机*2+侦察机  的目的地
int produce_state[2];   //第一个表示路，中路，中上，中下，上，下分别为0-4
						//第二个表示生产情况，生产顺序为潜艇，驱逐舰，飞机，飞机，侦察机
						//初始化为-1，0
int unit_union[4];   //即将生产出来的潜艇，驱逐舰，飞机，侦察机从属的集团，初始化为0 ；对于飞机，初始化为1，变为-1，变为2,变为-2等

enum CommandType
{
	//Produce
	PRODUCE,
	//Suppply
	SUPPLYFORT,
	SUPPLYBASE,
	SUPPLYUNIT,
	//Attack
	ATTACKUNIT,
	ATTACKFORT,
	ATTACKBASE,
	//Fix
    FIX,
	//ChangeDest
	FORWARD,
	CARGOSUPPLY,
	RETURNBASE,
	//Cancel
	CANCEL,
    kCommandTypes
};
void AIMain()
{  
init();
for(int i=0;i<INFO->element_num;i++)
	if(INFO->elements[i].team == INFO->team_num)
	{
		State Element = INFO->elements[i];
		Supply_Repair(i); //该补给或维修就去补给，维修
		Difference(i);    //判断刚出现的单位的从属
		Attack(i);        //攻击
		if(Element.type == BASE)
			BaseAct();     //基地维修及生产
		else if(Element.type == CARGO)
			Cargo_Supply(i);   //运输舰补给
		else ;
		Forward(i);       //前进
	}
MoveCargo();      //运输舰运动
delete []enemy_element;
}

//初始化定义各种量的函数
void init()
{
	for(int i = 0; i<INFO->element_num; i++)
		for(int j=0;j<2;j++)
			command[i][j] = -1;           //写一个初始化的函数
	parameter[0] = 0.1; parameter[0] = 0.3; parameter[0] = 0.3; parameter[0] = 0.2; parameter[0] = 0.5; 
	if(INFO->round == 1)
	{
		cargo_index[0] = -2; cargo_index[1] = -2;
		resource_defender[0] = -2; resource_defender[1] = -2;
		base_defender[0] = -2; base_defender[1] = -2;
		produce_state[0] = -1; produce_state[1] = 0;
		unit_union[0] = 0; unit_union[1] = 0; unit_union[2] = 0; unit_union[3] = 0;
		for(int i=0;i<5;i++)
		{	
			origin_target[0].x = 0;
			origin_target[0].x = 0;
			origin_target[0].x = 0;
		}

		//敌方单位构建
		enemy_num =0;
		for(int i=0;i<Info()->element_num;i++)
			if(Info()->elements[i].team != Info()->team_num)
				enemy_num += 1;
		enemy_element = new State[enemy_num];
		for(int i=0;i<Info()->element_num;i++)
			if(Info()->elements[i].team == 1-Info()->team_num ||
				(Info()->elements[i].type == FORT && Info()->elements[i].team != Info()->team_num))   //无主据点
				enemy_element[i] = Info()->elements[i];
		
	}
}

/////该补充燃料或者弹药的时候，或者血量太少需要回基地维修
void Supply_Repair(int i)
{
	State Element = INFO->elements[i];
	if(Element.health < parameter[0] * kElementInfos[Element.type].health_max && if_command(i, RETURNBASE))
	{
		ChangeDest(Element.index, INFO->elements[GetBase(INFO->team_num)].pos);
		command[i][1] = max(command[i][2], RETURNBASE);
	}
	else if((Element.ammo <  parameter[1]*kElementInfos[Element.type].ammo_max ||   //金属不足
		Element.fuel < parameter[2]*kElementInfos[Element.type].fuel_max)          //燃料不足
		&& if_command(i, CARGOSUPPLY))                                           //if_command
	    {
			int cargo_index = GetNear(Element.pos,CARGO);
			ChangeDest(INFO->elements[cargo_index].index, Element.pos);
			command[i][1] = CARGOSUPPLY;
		}
	else;
}

//返回pos1距pos2恰好相距fire_range的一个位置
Position minus(Position pos1,Position pos2,int fire_range)
{
	Position target;
	target.x = pos1.x > pos2.x ? pos1.x+(fire_range - distance(pos1,pos2))/2 : pos1.x -(fire_range - distance(pos1,pos2))/2;
	target.y = pos1.y > pos2.y ? pos1.y+((fire_range - distance(pos1,pos2))+1)/2 : pos1.y -((fire_range - distance(pos1,pos2))+1)/2;
	target.z = pos1.z;
	return target;

}

//计算攻击的伤害
int damage(State victim,State attacker)
{
	int fire_range = kElementInfos[attacker.type].fire_ranges[kElementInfos[victim.type].level];
	double coefficient = 1 - (distance(victim.pos,attacker.pos) - fire_range / 2) / (fire_range + 1) ;
	return (int)((kElementInfos[attacker.type].attacks[0] + kElementInfos[attacker.type].attacks[1])*coefficient 
		- (kElementInfos[attacker.type].defences[0] + kElementInfos[attacker.type].defences[1]));
}

//判断某个数是否在数组中
int if_in(int i,int *a,int len)
{
	for(int j=0;j<len;j++)
		if(i==a[j])
			return 1;
	return 0;
}

//获得己方或对方基地的索引
int GetBase(int team)
{
	const GameInfo *INFO = Info();
	int i;
	for(i=0; i<INFO->element_num; i++)
		if(INFO->elements[i].type == BASE && INFO->elements[i].team == team)
			return i; 
}

//两点之间的距离
int distance(Position pos1, Position pos2)
{
	return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y);
}

//判断某单位是否仍存活
int if_alive(int operand)
{
	for(int i=0;i<INFO->element_num;i++)
		if(INFO->elements[i].index == operand)
			return 1;
	return 0;
}

//最大值
int max(int x, int y)
{
	return x>y?x:y;
}

//获得距该位置最近的某类型单位的索引
int GetNear(Position pos, ElementType type)
{
	int i,near_index = -1,min_distance = 10000;
	for(i=0;i<INFO->element_num;i++)
		{
		if(INFO->elements[i].team == INFO->team_num && INFO->elements[i].type == type &&  distance(INFO->elements[i].pos, pos)<min_distance 
			&& type != OILFIELD && type!=MINE)
			{
				near_index = i;
				min_distance = distance(INFO->elements[i].pos, pos);
			}
		else if(INFO->elements[i].type == type &&  distance(INFO->elements[i].pos, pos)<min_distance   //保证油田有油
			&& type == OILFIELD && INFO->elements[i].fuel >= kElementInfos[CARGO].fuel_max)
		{
			near_index = i;
			min_distance = distance(INFO->elements[i].pos, pos);
		}
		else if(INFO->elements[i].type == type &&  distance(INFO->elements[i].pos, pos)<min_distance //保证矿场还有金属
			&& type == MINE  && INFO->elements[i].metal >= kElementInfos[CARGO].metal_max)
		{
			near_index = i;
			min_distance = distance(INFO->elements[i].pos, pos);
		}
		}
	return near_index;
}

//判断对该成员的该命令是否可以下达（如果已经下达更高级的指令则不可）
int if_command(int i,CommandType type,ElementType target = kElementTypes)
{
	if(INFO->elements[i].type != BASE && (type == PRODUCE || type == FIX))return 0;      //生产和维修操作
	if((INFO->elements[i].type >= FIGHTER || INFO->elements[i].type == SUBMARINE) && type <= SUPPLYUNIT)return 0;    //补给操作
	if(type < FORWARD && type > command[i][0])  //非移动指令
	{
		if((target == BASE || target == FORT || target == FIGHTER || target == SCOUT) && INFO->elements[i].type == SUBMARINE)
			return 0;                       // 潜艇打基地，据点，飞机不可
		if((INFO->elements[i].type == BASE || INFO->elements[i].type == FORT ) && target == SUBMARINE)
			return 0;                               //基地，据点打潜艇不可
		if(INFO->elements[i].type == CARGO && type < ATTACKUNIT) return 0; //运输舰没有攻击力
		return 1;
	}
	if(type >= FORWARD && type > command[i][1])  //移动指令
	{   
		if(INFO->elements[i].type == BASE || INFO->elements[i].type == FORT)return 0;//基地和据点不能移动
		return 1;
	}
	return 0;
}


//对于回合开始时相距为1的单位进行补给
void Cargo_Supply(int index)                           
{
	for(int j=0;j<INFO->element_num;j++)
		if(distance(INFO->elements[index].pos,INFO->elements[j].pos) <= 1 && index!=j && INFO->elements[index].team == INFO->team_num)
		{
			if(INFO->elements[index].type > OILFIELD)command[index][0] = SUPPLYUNIT;
			else if(INFO->elements[index].type == FORT)command[index][0] = SUPPLYFORT;
			else if(INFO->elements[index].type == BASE)command[index][0] = SUPPLYBASE;
			else continue;
			Supply(INFO->elements[index].index,INFO->elements[j].index,-1,-1,-1);
			break;
		}
}

//对于程序最后仍然没有命令的运输船，去资源点收集，或者回基地补给，或者呆在前线
void MoveCargo()        
{
	for(int i=0;i<INFO->element_num;i++)
		if(INFO->elements[i].type == CARGO && INFO->elements[i].team == INFO->team_num)
		{
		State Element = INFO->elements[i];
		if(command[i][1] == -1 )
			{
				if(Element.fuel < 0.5 * kElementInfos[CARGO].fuel_max)          //燃料不足
				{    ChangeDest(Element.index,INFO->elements[GetNear(Element.pos,OILFIELD)].pos);
					 command[i][1] = CARGOSUPPLY;
				}
				else if(Element.metal < 0.5 * kElementInfos[CARGO].metal_max)     //金属不足
				{	ChangeDest(Element.index,INFO->elements[GetNear(Element.pos,MINE)].pos);
					command[i][1] = CARGOSUPPLY;
				}
				else if(if_in(Element.index, cargo_index,2))         //是补给基地的船
				{	ChangeDest(Element.index,INFO->elements[GetBase(INFO->team_num)].pos);   
					command[i][1] = RETURNBASE;
				}	
				else                   //是补给前线的船
				{
					Forward(i);
				}
			}
		}
}

//寻找射程内的基地或据点，或选择血量最少的单位攻击,攻击后运动到距敌人恰好射程的地方
void Attack(int index)    
{
	State	Element = INFO->elements[index];
	int health = 1000,enemy_index = -1;
	if(!if_command(index,ATTACKBASE))return;
	for(int i=0;i<enemy_num;i++)
	{
		State enemy = INFO->elements[i];
		if(distance(Element.pos, enemy.pos) <= kElementInfos[Element.type].fire_ranges[kElementInfos[enemy.type].level])
		{	
			if((enemy.type == BASE || (enemy.type == FORT && enemy.team == 1-INFO->team_num)) && 
				if_command(index,CommandType(ATTACKBASE -(enemy.type-BASE)),ElementType(enemy.type)))                      //对方是基地或据点
			{
				AttackUnit(Element.index,enemy.index);
				command[index][0] = CommandType(ATTACKBASE -(enemy.type-BASE));
				if(if_command(index,FORWARD))
				{
					ChangeDest(Element.index,minus(Element.pos,enemy.pos,kElementInfos[Element.type].fire_ranges[kElementInfos[Element.type].level]));
					command[index][1] = FORWARD;
				}
				return;
			}
			if(enemy.type == FORT && enemy.team != 1-INFO->team_num  && enemy.health <= parameter[4]*kElementInfos[Element.type].attacks[0] 
				&& if_command(index,ATTACKFORT,FORT))                                     //无主据点
			{
				AttackUnit(Element.index,enemy.index);
				command[index][0] = ATTACKFORT;
				if(if_command(index,FORWARD))
				{
					ChangeDest(Element.index,minus(Element.pos,enemy.pos,kElementInfos[Element.type].fire_ranges[kElementInfos[Element.type].level]));
					command[index][1] = FORWARD;
				}
				return;
			}
			if(health>enemy.health)   
			{
				health=enemy.health;
				enemy_index=i;
			}
		}
	}
	if(enemy_index != -1 && if_command(index,ATTACKUNIT,ElementType(INFO->elements[enemy_index].type)))
	{
		AttackUnit(Element.index,INFO->elements[enemy_index].index);
		command[index][0] = ATTACKUNIT;
		if(if_command(index,FORWARD))
		{
			ChangeDest(Element.index,minus(Element.pos,INFO->elements[enemy_index].pos,kElementInfos[Element.type].fire_ranges[kElementInfos[Element.type].level]));
			command[index][1] = FORWARD;
		}
	}
}

//基地的维修，生产
void BaseAct()
{
	int index,health=1000;
	for(int i=0;i<INFO->element_num;i++)
	{
		if(distance(INFO->elements[i].pos,INFO->elements[GetBase(INFO->team_num)].pos)<=1 && 
			INFO->elements[i].health < parameter[5]*kElementInfos[INFO->elements[i].type].health_max
			&& health>INFO->elements[i].health && INFO->elements[i].team == INFO->team_num)
		{
			index = i;
			health = INFO->elements[i].health;
		}
	}
	if(if_command(GetBase(INFO->team_num),FIX) && health != 1000)
	{	
		Fix(INFO->elements[GetBase(INFO->team_num)].index,index);
		command[GetBase(INFO->team_num)][0] = FIX;
		return;
	}
		BaseProduce();   //生产命令
}

///基地的生产
void BaseProduce()
{
	int index = GetBase(INFO->team_num);
	State Element =INFO->elements[index];
	if(!if_command(index,PRODUCE))return;
	for(int i=0; i<2;i++)        //判断补给基地的两条船是否存活，不存活则直接生产运输舰
	{
		if(cargo_index[i] == -2 || (cargo_index[i]>=0 && !if_alive(cargo_index[i])))
		{
			Produce(Element.index,CARGO);
			command[index][0] = PRODUCE;
			cargo_index[i] = -1;
			return;
		}
	} 

	//中间三路的生产
	if(produce_state[0]<3 && produce_state[1]<= 4)         
		switch(produce_state[1])
		{
			case 0:Produce(Element.index,SUBMARINE);command[index][0] = PRODUCE;produce_state[1] += 1;return;
			case 1: Produce(Element.index,DESTROYER);command[index][0] = PRODUCE;produce_state[1] += 1;return;
			case 2:
			case 3: Produce(Element.index,FIGHTER);command[index][0] = PRODUCE;produce_state[1] += 1;return;
			case 4: Produce(Element.index,SCOUT);command[index][0] = PRODUCE;produce_state[0] += 1; return;
			default:;
		}

	 //上下路的生产
	if(produce_state[0]>= 3 && produce_state[0]<5 && produce_state[1] <= 2)        
		switch(produce_state[1])
		{
			case 0:
			case 1: Produce(Element.index,FIGHTER);command[index][0] = PRODUCE;produce_state[1] += 1;return;
			case 2: Produce(Element.index,SCOUT);command[index][0] = PRODUCE;produce_state[1] += 1;return;
			default:;
		}

	 //在中路和中下路生产完后各生产一条运输船
	if((produce_state[0] == 1 || produce_state[0] == 3 )&& produce_state[1] == 5)    
	{
		Produce(Element.index,CARGO);
		command[index][0] = PRODUCE;
		produce_state[0] += 1;
		produce_state[1] = 0;
		return;
	}

	//在中上路，和上路生产完后，生产战斗机去防守资源
	if((produce_state[0] == 2 || produce_state[0] == 4)&& produce_state[1] == 5 && resource_defender[1] == -2 )
	{															
		int i = resource_defender[0] == -2 ? 0 : 1;
		Produce(Element.index,FIGHTER);
		command[index][0] = PRODUCE;
		resource_defender[i] = -1;
		produce_state[0] += 1;
		if(produce_state[0] == 5)produce_state[0] = 1;
		produce_state[1] = 0;
		return;
	}

	//生产潜艇防守基地
	if(INFO->round > 5 && produce_state[0] == 0 && produce_state[1] == 5 && base_defender[1] == -2) 
	{
		int i = base_defender[0] == -2 ? 0 : 1;
		Produce(Element.index,SUBMARINE);
		command[index][0] = PRODUCE;
		resource_defender[i] = -1;
		produce_state[0] += 1;
	}

}

////寻找最近的敌军前进，如果是运输船
void Forward(int index)
{
	State Element = INFO->elements[index];
	int Distance=1000; 
	Position target;
	if(!if_command(index,FORWARD))return;
	if(Element.type == BASE || Element.type == FORT)
		return;
	else if(Element.type == CARGO)
	{
		for(int i=0;i<INFO->element_num;i++)
			if(distance(Element.pos,INFO->elements[i].pos) < Distance && index!=i && INFO->elements[index].team == INFO->team_num)
			{
				Distance = distance(Element.pos,INFO->elements[i].pos) < Distance;
				target = INFO->elements[i].pos;
			}
	}
	else
	{
		for(int i=0;i<enemy_num;i++)
			if(distance(Element.pos,enemy_element[i].pos) < Distance && index!=i)
			{
				Distance = distance(Element.pos,enemy_element[i].pos) < Distance;
				target = enemy_element[i].pos;
			}
	}
	ChangeDest(Element.index,target);
	command[index][1] = FORWARD;
}

//判断刚被生产出来的时候单位的从属
void Difference(int index)
{
	State Element = INFO->elements[index];
	switch(Element.type)
	{
	case BASE:break;
	case FORT:break;
	case CARGO:
		for(int i=0;i<=1;i++)     //判断是否为刚生产出来的补给基地的运输船
			if(cargo_index[i] == -1 && distance(Element.pos,INFO->elements[GetBase(INFO->team_num)].pos) <= 1)
			{
				cargo_index[i] = Element.index;
				return;
			}
		return;
	case SUBMARINE:
		for(int i=0;i<2;i++)
			if(base_defender[i] == -1 && distance(Element.pos,INFO->elements[GetBase(INFO->team_num)].pos) <= 1)
			{
				base_defender[i] = Element.index;
				return;
			}
		ChangeDest(Element.index,origin_target[unit_union[0]]);
		if(unit_union[0] == 4)
			unit_union[0] = 0;
		else unit_union[0] += 1;
		return;
	case DESTROYER:
		ChangeDest(Element.index,origin_target[unit_union[1]]);
		if(unit_union[1] == 4)
			unit_union[1] = 0;
		else unit_union[1] += 1;
		return;
	case FIGHTER:
		ChangeDest(Element.index,origin_target[abs(unit_union[1])-1]);
		if(unit_union[2] > 0)
			unit_union[2] = -unit_union[2];
		else if(unit_union[2] == -5) 
			unit_union[2] = 1;
		else 
			unit_union[2] = -unit_union[2] + 1;
		return;
	case SCOUT:
		ChangeDest(Element.index,origin_target[abs(unit_union[1])-1]);
		if(unit_union[3] == 4)
			unit_union[3] = 0;
		else unit_union[3] += 1;
		return;
	}

}