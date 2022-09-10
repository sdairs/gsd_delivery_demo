<script>
	import 'carbon-components-svelte/css/g100.css';
	import '@carbon/charts/styles.css';
	import {
		Header,
		HeaderUtilities,
		HeaderAction,
		HeaderPanelLinks,
		HeaderPanelDivider,
		HeaderPanelLink,
		Content,
		Grid,
		Row,
		Column,
		Link
	} from 'carbon-components-svelte';

	let isOpen = false;
	let transition = { duration: 200 };
</script>

<Header company="Tinybird" platformName="Parcel Company">
	<HeaderUtilities>
		<HeaderAction bind:isOpen {transition}>
			<HeaderPanelLinks>
				<HeaderPanelDivider>Internal Apps</HeaderPanelDivider>
				<HeaderPanelLink>
					<Link href="/internal/operational_dashboard">Operational Dashboard</Link>
				</HeaderPanelLink>
				<HeaderPanelLink>
					<Link href="/internal/customer_service">Customer Service</Link>
				</HeaderPanelLink>
				<HeaderPanelDivider>External Apps</HeaderPanelDivider>
				<HeaderPanelLink>
					<Link href="/external/parcel_tracker">Parcel Tracker</Link>
				</HeaderPanelLink>
				<HeaderPanelLink>
					<Link href="/external/parcel_order">Parcel Order</Link>
				</HeaderPanelLink>
			</HeaderPanelLinks>
		</HeaderAction>
	</HeaderUtilities>
</Header>

<Content>
	<Grid>
		<Row>
			<Column>
				<slot />
			</Column>
		</Row>
	</Grid>
</Content>
