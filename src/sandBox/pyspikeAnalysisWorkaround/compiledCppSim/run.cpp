#include<stdlib.h>
#include "objects.h"
#include<ctime>

#include "code_objects/neurongroup_resetter_codeobject.h"
#include "code_objects/neurongroup_stateupdater_codeobject.h"
#include "code_objects/neurongroup_thresholder_codeobject.h"
#include "code_objects/poissongroup_thresholder_codeobject.h"
#include "code_objects/spikemonitor_1_codeobject.h"
#include "code_objects/spikemonitor_codeobject.h"
#include "code_objects/statemonitor_1_codeobject.h"
#include "code_objects/statemonitor_codeobject.h"
#include "code_objects/synapses_group_variable_set_conditional_codeobject.h"
#include "code_objects/synapses_post_codeobject.h"
#include "code_objects/synapses_post_initialise_queue.h"
#include "code_objects/synapses_post_push_spikes.h"
#include "code_objects/synapses_pre_codeobject.h"
#include "code_objects/synapses_pre_initialise_queue.h"
#include "code_objects/synapses_pre_push_spikes.h"
#include "code_objects/synapses_stateupdater_codeobject.h"
#include "code_objects/synapses_synapses_create_generator_codeobject.h"


void brian_start()
{
	_init_arrays();
	_load_arrays();
	// Initialize clocks (link timestep and dt to the respective arrays)
    brian::defaultclock.timestep = brian::_array_defaultclock_timestep;
    brian::defaultclock.dt = brian::_array_defaultclock_dt;
    brian::defaultclock.t = brian::_array_defaultclock_t;
    brian::statemonitor_1_clock.timestep = brian::_array_statemonitor_1_clock_timestep;
    brian::statemonitor_1_clock.dt = brian::_array_statemonitor_1_clock_dt;
    brian::statemonitor_1_clock.t = brian::_array_statemonitor_1_clock_t;
    brian::statemonitor_clock.timestep = brian::_array_statemonitor_clock_timestep;
    brian::statemonitor_clock.dt = brian::_array_statemonitor_clock_dt;
    brian::statemonitor_clock.t = brian::_array_statemonitor_clock_t;
	srand((unsigned int)time(NULL));
	rand(); // put this in because the first random number generated on some versions of C++ is always almost the same
}

void brian_end()
{
	_write_arrays();
	_dealloc_arrays();
}

